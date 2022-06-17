load("@pip//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")
visibility = ["//visibility:public"]

py_library(
    name = "grow_request_builder",
    srcs = ["grow_request_builder.py"],
    deps = [
    ],
    visibility = ["//visibility:public"]
)

py_library(
    name = "request_factory",
    srcs = ["request_factory.py"],
    deps = [
        "//proto:grow_grpc",
#        "//:grow_request_builder",
    ],
    visibility = ["//visibility:public"]
)



filegroup(
    name = "libs",
    srcs = glob(["rpc_client/libs/*.py"]),
    visibility = ["//visibility:public"]
)