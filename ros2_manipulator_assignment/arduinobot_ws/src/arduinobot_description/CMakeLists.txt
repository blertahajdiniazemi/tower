cmake_minimum_required(VERSION 3.5)
project(arduinobot_description)


find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch meshes urdf rviz
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # The source files carry no per-file copyright headers (the package is
  # licensed as a whole, see package.xml), so the copyright linter is skipped.
  set(ament_cmake_copyright_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
