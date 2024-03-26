# from typing import Callable

# def add_text(fn: Callable):

#     def wrapper(*args, **kwargs):
#         name = fn(*args, **kwargs)
#         print(f"My name is {name}")
#         return name

#     return wrapper

# # @add_text
# # def take_name(name: str) -> str:
# #     return name

# # print(take_name("Slim shady"))



# class Letters:
#     def __init__(self, name: str) -> None:
#         self.name = name

#     @add_text
#     def upper_case(self) -> str:
#         return self.name.upper()

#     @add_text
#     def lower_case(self) -> str:
#         return self.name.lower()[::-1]

#     @add_text
#     def split_string(self) -> list:
#         return [*self.name]


# first_try = Letters(name="Vilius")

# first_try.upper_case(), first_try.lower_case(), first_try.split_string()