PROJECT(rdjpgcom C CXX)
cmake_minimum_required(VERSION 2.8)

include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

ADD_EXECUTABLE(rdjpgcom rdjpgcom.c)
TARGET_LINK_LIBRARIES(rdjpgcom ${CONAN_LIBS})
