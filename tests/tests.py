def print_kwargs(**args):
    count = 0
    for x in args:
        print(count, x, args[x])
        count += 1

        # print("The value of {} is {}".format(key, value))


print_kwargs(kwargs_1="Shark", kwargs_2=4.5, kwargs_3=True)


# def concatenate(**kwargs):
#     result = ""
#     # Iterating over the Python kwargs dictionary
#     for arg in kwargs.values():
#         result += arg
#     return result
#
#
# print(concatenate(a="Real", b="Python", c="Is", d="Great", e="!"))
#
#
# def my_sum(*integers):
#     result = 0
#     for x in integers:
#         result += x
#     return result
#
#
# print(my_sum(1, 2, 3))
