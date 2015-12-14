from conans import ConanFile
import os
from conans.tools import download, unzip, replace_in_file
from conans import CMake


class libjpegConan(ConanFile):
    name = "libjpeg"
    version = "8.3"
    LIBJPEG_FOLDER_NAME = "libjpeg"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {}
    default_options = ""
    exports = "CMakeLists.txt", "libjpeg/*"
    url="http://github.com/mathieu/conan-libjpeg"
    # requires ="zlib/1.2.8@lasote/stable"

    def conan_info(self):
        # We don't want to change the package for each compiler version but
        # we need the setting to compile with cmake
        self.info.settings.compiler.version = "any"

    def source(self):
        self.download_url = "http://ijg.org/files/jpegsr8c.zip"

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            self.run("IF not exist build mkdir build")
        else:
            self.run("mkdir build")
        cd_build = "cd build"
        self.output.warn('%s && cmake .. %s' % (cd_build, cmake.command_line))
        self.run('%s && cmake .. %s' % (cd_build, cmake.command_line))
        self.output.warn("%s && cmake --build . %s" % (cd_build, cmake.build_config))
        self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))

    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        # Copying libjpeg.h, zutil.h, zconf.h
        self.copy("*.h", "include", "%s" % (self.LIBJPEG_FOLDER_NAME), keep_path=False)
        self.copy("*.h", "include", "%s" % ("_build"), keep_path=False)

        # Copying static and dynamic libs
        if self.settings.os == "Windows":
            self.copy(pattern="libjpegd.lib", dst="lib", src="build/lib", keep_path=False)
            self.copy(pattern="libjpeg.lib", dst="lib", src="build/lib", keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", src="build/lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ['libjpegd']
            else:
                self.cpp_info.libs = ['libjpeg']
        else:
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ['jpegd']
            else:
                self.cpp_info.libs = ['jpeg']
