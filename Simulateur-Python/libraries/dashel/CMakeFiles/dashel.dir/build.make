# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.12

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/cmake-3.12.4/bin/cmake

# The command to remove a file.
RM = /usr/local/cmake-3.12.4/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel-src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel

# Include any dependencies generated for this target.
include CMakeFiles/dashel.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/dashel.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/dashel.dir/flags.make

CMakeFiles/dashel.dir/dashel/dashel-posix.cpp.o: CMakeFiles/dashel.dir/flags.make
CMakeFiles/dashel.dir/dashel/dashel-posix.cpp.o: /home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel-src/dashel/dashel-posix.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/dashel.dir/dashel/dashel-posix.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/dashel.dir/dashel/dashel-posix.cpp.o -c /home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel-src/dashel/dashel-posix.cpp

CMakeFiles/dashel.dir/dashel/dashel-posix.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dashel.dir/dashel/dashel-posix.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel-src/dashel/dashel-posix.cpp > CMakeFiles/dashel.dir/dashel/dashel-posix.cpp.i

CMakeFiles/dashel.dir/dashel/dashel-posix.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dashel.dir/dashel/dashel-posix.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel-src/dashel/dashel-posix.cpp -o CMakeFiles/dashel.dir/dashel/dashel-posix.cpp.s

CMakeFiles/dashel.dir/dashel/dashel-common.cpp.o: CMakeFiles/dashel.dir/flags.make
CMakeFiles/dashel.dir/dashel/dashel-common.cpp.o: /home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel-src/dashel/dashel-common.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/dashel.dir/dashel/dashel-common.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/dashel.dir/dashel/dashel-common.cpp.o -c /home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel-src/dashel/dashel-common.cpp

CMakeFiles/dashel.dir/dashel/dashel-common.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dashel.dir/dashel/dashel-common.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel-src/dashel/dashel-common.cpp > CMakeFiles/dashel.dir/dashel/dashel-common.cpp.i

CMakeFiles/dashel.dir/dashel/dashel-common.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dashel.dir/dashel/dashel-common.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel-src/dashel/dashel-common.cpp -o CMakeFiles/dashel.dir/dashel/dashel-common.cpp.s

# Object files for target dashel
dashel_OBJECTS = \
"CMakeFiles/dashel.dir/dashel/dashel-posix.cpp.o" \
"CMakeFiles/dashel.dir/dashel/dashel-common.cpp.o"

# External object files for target dashel
dashel_EXTERNAL_OBJECTS =

libdashel.so.1.1.0: CMakeFiles/dashel.dir/dashel/dashel-posix.cpp.o
libdashel.so.1.1.0: CMakeFiles/dashel.dir/dashel/dashel-common.cpp.o
libdashel.so.1.1.0: CMakeFiles/dashel.dir/build.make
libdashel.so.1.1.0: /usr/lib/x86_64-linux-gnu/libudev.so
libdashel.so.1.1.0: CMakeFiles/dashel.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX shared library libdashel.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/dashel.dir/link.txt --verbose=$(VERBOSE)
	$(CMAKE_COMMAND) -E cmake_symlink_library libdashel.so.1.1.0 libdashel.so.1 libdashel.so

libdashel.so.1: libdashel.so.1.1.0
	@$(CMAKE_COMMAND) -E touch_nocreate libdashel.so.1

libdashel.so: libdashel.so.1.1.0
	@$(CMAKE_COMMAND) -E touch_nocreate libdashel.so

# Rule to build all files generated by this target.
CMakeFiles/dashel.dir/build: libdashel.so

.PHONY : CMakeFiles/dashel.dir/build

CMakeFiles/dashel.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/dashel.dir/cmake_clean.cmake
.PHONY : CMakeFiles/dashel.dir/clean

CMakeFiles/dashel.dir/depend:
	cd /home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel-src /home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel-src /home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel /home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel /home/travis/build/omichel/webots/projects/robots/mobsya/thymio/libraries/dashel/CMakeFiles/dashel.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/dashel.dir/depend

