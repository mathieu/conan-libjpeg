import os
import platform
import sys
from subprocess import Popen, PIPE

if __name__ == "__main__":
    os.system('conan export mathieu/stable')

    def test(settings):
        argv =  " ".join(sys.argv[1:])
        command = "conan test %s %s" % (settings, argv)
        retcode = os.system(command)
        if retcode != 0:
            exit("Error while executing:\n\t conan %s" % args)


    if platform.system() == "Windows":
        compiler = '-s compiler="Visual Studio" -s compiler.version=14 '
        # Static x86
        test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MDd ')
        test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MD ')

        # Static x86_64
        test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MDd ')
        test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MD ')


    else:  # Compiler and version not specified, please set it in your home/.conan/conan.conf (Valid for Macos and Linux)
        # if not os.getenv("TRAVIS", False):
        #     # Static x86
        #     test('-s arch=x86 -s build_type=Debug -o libjpeg:shared=False')
        #     test('-s arch=x86 -s build_type=Release -o libjpeg:shared=False')
        #
        #     # Shared x86
        #     test('-s arch=x86 -s build_type=Debug -o libjpeg:shared=True')
        #     test('-s arch=x86 -s build_type=Release -o libjpeg:shared=True')

        # Static x86_64
        test('-s arch=x86_64 -s build_type=Debuge ')
        test('-s arch=x86_64 -s build_type=Release ')
