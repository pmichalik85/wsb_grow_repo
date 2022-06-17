load("@bazel_tools//tools/build_defs/pkg:pkg.bzl", "pkg_tar")
visibility = ["//visibility:public"]
pkg_tar(
    name = "server_pkg",
    strip_prefix = "",
    package_dir = "/server_pkg",
    srcs = [
        "//server:init_script",
        "//server:grow",
        "//server:grow_lib",
        "//proto:grow_grpc",
        "//proto:grow_grpc_proto",
        "//proto:grow_grpc_py_proto"],

    mode = "0755",
)