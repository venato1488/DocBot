def print_kwargs(**kwargs):
    for key, value in kwargs.items():
        print(f"{key} = {value}")

print_kwargs(name="John", age=25, city="New York") 
# Output: name = John, age = 25, city = New York
