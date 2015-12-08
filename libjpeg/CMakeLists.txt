set(the_target "jpeg")
project(${the_target} C)
enable_testing()
cmake_minimum_required(VERSION 2.8)

include_directories(
	${CMAKE_CURRENT_SOURCE_DIR}
	)

# The .cpp files:
file(GLOB lib_srcs
    jaricom.c
    jcapimin.c
    jcapistd.c
    jcarith.c
    jccoefct.c
    jccolor.c
    jcdctmgr.c
    jchuff.c
    jcinit.c
    jcmainct.c
    jcmarker.c
    jcmaster.c
    jcomapi.c
    jcparam.c
    jcprepct.c
    jcsample.c
    jctrans.c
    jdapimin.c
    jdapistd.c
    jdarith.c
    jdatadst.c
    jdatasrc.c
    jdcoefct.c
    jdcolor.c
    jddctmgr.c
    jdhuff.c
    jdinput.c
    jdmainct.c
    jdmarker.c
    jdmaster.c
    jdmerge.c
    jdpostct.c
    jdsample.c
    jdtrans.c
    jerror.c
    jfdctflt.c
    jfdctfst.c
    jfdctint.c
    jidctflt.c
    jidctfst.c
    jidctint.c
    jmemmgr.c
    jmemnobs.c
    jquant1.c
    jquant2.c
	jutils.c
)

file(GLOB lib_hdrs *.h)

# ----------------------------------------------------------------------------------
# 				Define the library target:
# ----------------------------------------------------------------------------------

set(JPEGLIB_MAJOR 8)
set(JPEGLIB_MINOR 3)
set(JPEGLIB_NAME ${the_target})
set(JPEGLIB_VERSION ${JPEGLIB_MAJOR}.${JPEGLIB_MINOR})

# to distinguish between debug and release lib
set(CMAKE_DEBUG_POSTFIX "d")

include_directories(${CMAKE_CURRENT_BINARY_DIR})

if(SHARED_LIB)
	add_library(${JPEGLIB_NAME} SHARED ${lib_srcs})
else()
	add_library(${JPEGLIB_NAME} STATIC ${lib_srcs})
endif()

if(MSVC)
  # msvc does not append 'lib' - do it here to have consistent name
  set_target_properties(${JPEGLIB_NAME} PROPERTIES PREFIX "lib")
  add_definitions(-DJPEG_NO_MODULEDEF -D_CRT_SECURE_NO_DEPRECATE)
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} /W3")
endif()
#target_link_libraries(${JPEGLIB_NAME} )

#
# Set a variable with CMake code which:
# Creates a symlink from src to dest (if possible) or alternatively
# copies if different.
macro(_jpeg_generate_symlink_code CODE SRC DEST)
  if(WIN32 AND NOT CYGWIN)
    set(_jpeg_gsc_message "Copying ${SRC} to ${DEST} if needed")
    set(_jpeg_gsc_operation "copy_if_different")
  else()
    set(_jpeg_gsc_message "Symlinking ${SRC} to ${DEST}")
    set(_jpeg_gsc_operation "create_symlink")
  endif()

  set(${CODE} "
    message(STATUS \"${_jpeg_gsc_message}\")
    execute_process(COMMAND \${CMAKE_COMMAND} -E ${_jpeg_gsc_operation}
      \"${SRC}\" \"${DEST}\")
    ")
endmacro()

# CREATE PKGCONFIG FILES
# we use the same files like ./configure, so we have to set its vars
if(NOT DEFINED CMAKE_INSTALL_LIBDIR)
  set(CMAKE_INSTALL_LIBDIR lib)
endif(NOT DEFINED CMAKE_INSTALL_LIBDIR)
set(prefix      ${CMAKE_INSTALL_PREFIX})
set(exec_prefix ${CMAKE_INSTALL_PREFIX})
set(libdir      ${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR})
set(includedir  ${CMAKE_INSTALL_PREFIX}/include)
set(LIBS        "-lz -lm")
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/libjpeg.pc.in
  ${CMAKE_CURRENT_BINARY_DIR}/${JPEGLIB_NAME}.pc @ONLY)
_jpeg_generate_symlink_code(JPEG_PC_INSTALL_CODE
  ${CMAKE_CURRENT_BINARY_DIR}/${JPEGLIB_NAME}.pc
  ${CMAKE_CURRENT_BINARY_DIR}/libjpeg.pc)
install(CODE ${JPEG_PC_INSTALL_CODE})

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/libjpeg-config.in
  ${CMAKE_CURRENT_BINARY_DIR}/${JPEGLIB_NAME}-config @ONLY)
_jpeg_generate_symlink_code(JPEG_CONFIG_INSTALL_CODE
  ${CMAKE_CURRENT_BINARY_DIR}/${JPEGLIB_NAME}-config
  ${CMAKE_CURRENT_BINARY_DIR}/libjpeg-config)
install(CODE ${JPEG_CONFIG_INSTALL_CODE})

  # MSVC doesn't use a different file extension for shared vs. static
  # libs.  We are able to change OUTPUT_NAME to remove the _static
  # for all other platforms.
  if(NOT MSVC)
    set_target_properties(${JPEGLIB_NAME} PROPERTIES
      OUTPUT_NAME ${JPEGLIB_NAME}
      CLEAN_DIRECT_OUTPUT 1)
  endif()

# If CMake > 2.4.x, we set a variable used below to export
# targets to an export file.
# TODO: Use VERSION_GREATER after our cmake_minimum_required >= 2.6.2
if(CMAKE_MAJOR_VERSION GREATER 1 AND CMAKE_MINOR_VERSION GREATER 4)
  set(JPEG_EXPORT_RULE EXPORT libjpeg)
elseif(CMAKE_MAJOR_VERSION GREATER 2) # future proof
  set(JPEG_EXPORT_RULE EXPORT libjpeg)
endif()

# INSTALL
if(NOT SKIP_INSTALL_LIBRARIES AND NOT SKIP_INSTALL_ALL )

    install(TARGETS ${JPEGLIB_NAME}
        ${JPEG_EXPORT_RULE}
            LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
            ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
    if(NOT WIN32 OR CYGWIN)
      IF(CMAKE_ARCHIVE_OUTPUT_DIRECTORY)
         _jpeg_generate_symlink_code(JPEG_STATIC_INSTALL_CODE
${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}/${JPEGLIB_NAME}${CMAKE_STATIC_LIBRARY_SUFFIX}
        ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}/libjpeg${CMAKE_STATIC_LIBRARY_SUFFIX})
        install(CODE ${JPEG_STATIC_INSTALL_CODE})
        install(FILES
          ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY}/libjpeg${CMAKE_STATIC_LIBRARY_SUFFIX}
             DESTINATION ${CMAKE_INSTALL_LIBDIR})
      ELSE(CMAKE_ARCHIVE_OUTPUT_DIRECTORY)
        _jpeg_generate_symlink_code(JPEG_STATIC_INSTALL_CODE
           ${JPEGLIB_NAME}${CMAKE_STATIC_LIBRARY_SUFFIX}
           libjpeg${CMAKE_STATIC_LIBRARY_SUFFIX})
        install(CODE ${JPEG_STATIC_INSTALL_CODE})
        install(FILES
          ${CMAKE_CURRENT_BINARY_DIR}/libjpeg${CMAKE_STATIC_LIBRARY_SUFFIX}
                     DESTINATION ${CMAKE_INSTALL_LIBDIR})
      ENDIF(CMAKE_ARCHIVE_OUTPUT_DIRECTORY)
    endif()
endif()

if(NOT SKIP_INSTALL_HEADERS AND NOT SKIP_INSTALL_ALL )
  install(FILES ${lib_hdrs}   DESTINATION include)
endif()

# what's with libjpeg-$VER%.txt and all the extra files?


# UNINSTALL
# do we need this?


# DIST
# do we need this?

# to create msvc import lib for mingw compiled shared lib
# pexports libjpeg.dll > libjpeg.def
# lib /def:libjpeg.def /machine:x86
