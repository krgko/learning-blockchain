# Learning blockchain

This project all about learning blockchain with consensus algorithm PoW (Proof of Work)

> If we understand this we will able to develop blockchain with any language

## Start App

```bash
python3 node.py
```

- [Learning blockchain](#learning-blockchain)
  - [Start App](#start-app)
  - [Requirement](#requirement)
  - [REPL](#repl)
  - [Blockchain](#blockchain)
    - [Properties](#properties)
    - [Security layer](#security-layer)
  - [Proof of work](#proof-of-work)
    - [Process](#process)
    - [Cheating](#cheating)
  - [Important note](#important-note)
  - [New things learned from python](#new-things-learned-from-python)
    - [Variable](#variable)
    - [Casting](#casting)
    - [Number-operation](#number-operation)
    - [Weird behavior of python number](#weird-behavior-of-python-number)
    - [List](#list)
    - [Function](#function)
    - [Default argument](#default-argument)
    - [Variable scope](#variable-scope)
    - [comment for document](#comment-for-document)
    - [loop](#loop)
    - [if-else](#if-else)
    - [continue-break](#continue-break)
    - [not](#not)
    - [and,or](#andor)
    - [grouping conditions](#grouping-conditions)
    - [switch case](#switch-case)
    - [is & in](#is--in)
    - [For loop with else](#for-loop-with-else)
    - [Range](#range)
    - [While](#while)
    - [List and String](#list-and-string)
    - [Format](#format)
    - [Escape String](#escape-string)
    - [DS-List](#ds-list)
    - [Set](#set)
    - [Tuple](#tuple)
    - [Dictionary](#dictionary)
    - [Enumerate](#enumerate)
    - [Copiled other complex type](#copiled-other-complex-type)
    - [Shallow vs deep copies](#shallow-vs-deep-copies)
    - [is and ==](#is-and)
    - [All and Any](#all-and-any)
    - [Comparison between data structures (python)](#comparison-between-data-structures-python)
    - [List comprehension](#list-comprehension)
    - [Lambda function](#lambda-function)
    - [Reducing list](#reducing-list)
    - [Import](#import)
    - [Unpack argument of function](#unpack-argument-of-function)
    - [Importing](#importing)
    - [Handling File Access](#handling-file-access)
    - [Instead of JSON change to Binary](#instead-of-json-change-to-binary)
    - [Pickle vs JSON](#pickle-vs-json)
    - [Debugger](#debugger)
    - [Try-except](#try-except)
    - [Which one should handle](#which-one-should-handle)
    - [OOP](#oop)
      - [VS Dict](#vs-dict)
      - [Why need OOP](#why-need-oop)
    - [OOP example with inheritance](#oop-example-with-inheritance)
    - [Instance vs Class vs Static methods & attibutes](#instance-vs-class-vs-static-methods--attibutes)
    - [Private attribute](#private-attribute)
    - [Attribute vs Properties](#attribute-vs-properties)
    - [The Modules](#the-modules)
    - [pycache](#pycache)
    - [Controlling exports](#controlling-exports)
    - [Special variable **name**](#special-variable-name)

## Requirement

1. Python 3.x
2. Time

## REPL

Command line approch contains with

- Read - read variable
- Eval - like calculate, operate
- Print - print the result
- Loop - do it again

## Blockchain

- **Transactions:** in this case it will store data like coin
  1. sender
  2. recipient
  3. amount/data
- **Blocks:** wrapper transaction(s) with header and append to chain - occur by mining (put transactions and pack as block)
- **Blockchain:** multiple block that appended start from first block(genesis block) like chain (data structure like link-list)
- **Hash:** use for reference block like an id. it stored on header of block(previous hase, current hash)
  - **Why hash needed in blockchain**: if need to verify using previous transaction as chain there are many transactions and it very long so hashing can help to represent data to strings for using in verify step
- **Nonce (Number Used Once):** use for prevent replay request for PoW it used to check validity for miner who won puzzle solving as well
- **Merkle Tree (data structure)** - use to check correctly of transaction in block and make sure that does not modified (a.k.a checksum) - some blockchain generate hash from merkle root
- **Data structure** - maybe key-store, ...

- **Maniplate the chain** the blockchain does not allow to modify some data on the chain and the chain will invalid
- **Blockchain verification** It use hash that calculate each block this will ensure that chain cannot manipulated
- **To verify block hashes** Can check by try to create another set of hash as current_hash and reconcile with previous_hash
- **Private key and Public key** Used for manipulated data (for prevent change from unauthorized user), also for construct wallet. The private key use for sign transaction as signature. And The public key used to verify transaction that created by private key

### Properties

- Immutability: Cannot be mutate
- Decentralized: Support running on multiple parties with the same context of storage
- Transparency: Every block can verify and broadcast publicly

### Security layer

- Block know each other: Manipulated check - Check previous hash
- Mine block require by [PoW](#proof-of-work): No mass production allowed
- Transaction need to be signed

## Proof of work

Mining is challenging -> for security and control amount of coins

- Find a number which fullfill PoW requirement (Answer of puzzle)
- Take block data into account -> **If number is correct will added to block metadata then commit with transaction and previous hash**
- Other node can verify PoW easily

### Process

- Transactions - difference from Nonce
- Previous hash
- Proof (Nonce: Number used once) - increment in loop 0, ... n
  Checking PoW by hash all above into a hash e.g `00[a-f0-9]{62}` 00 is difficulty - miner need to find a correct hash

### Cheating

Add old block -> check hash will failed to matched with previous hash
Nonce changed -> that is a part of hash all of hashes after cheated block will change and PoW takes time so, all the block will be recalculated (These step will occur with block has been validated)

## Important note

- Python code indentation is the most significant. developers need to care about

## New things learned from python

### Variable

assign variable python has no data type(weak type)

```py
  variable = 'string' # string
  variable = 1        # int
  variable = 1.2      # float
  variable = True     # boolean
```

### Casting

make current type to target type

```py
  int(12), str(12) # type string
```

### Number-operation

```py
  +, - , * , /
  ** - power
  // - divide with floor
  % - modulo
```

**Note:** +, \* can be worked with string to concatenate or iterate

### Weird behavior of python number

if number cannot divide that got finite degit and do operation like `1-0.9 the answer will be 0.0999999998`

### List

or array on other programming language

```py
  list.append() - append element to list
  list.remove(index) - remove with index
  list.pop() - pop element from list

  # accessing last element in list for python
  # list[-1]
```

### Function

wrapper of codes for calling more than once

```py
  def function_name():
      ...
      return {something}
```

### Default argument

```py
  def function_name(variable1='something_any_type'):
      ...
```

### Variable scope

contains with 2 types are global and local

```py
  name = input('name: ') # 'xx'

  def name_mod():
      """ Name will not change """
      name = 'yy' # name does not changed

  def name_mod_global():
      """ Name will change """
      global name
      name = 'yy' # name changed
```

**Note:** Why function cannot change? because python always create local variable with variable declared inside function scope

### comment for document

create comment by use """(triple double quotes)

### loop

python contains for loop and while loop

```py
  # iterate through elements list
  for elem in list:
    ...

  # repeat code until true
  while True:
    ...
```

### if-else

condition like other language

```py
  if condition:
    ...
  elif condition:
    ...
  else:
    ...
```

### continue-break

this keyward will be in for-loop or while loop

```py
  # end current iterate and continue iteration
  continue

  # end loop
  break
```

### not

use for check in negative case work only string case

```py
  if char not in str:
    ...
```

### and,or

use for join condition, the result can check from truty table

```py
  condition_1 and condition_2
  condition_1 or condition_2
```

### grouping conditions

conditions can be combined to check like

```py
  (condition_1 {logic} condition_2) {logic} condition_3
```

### switch case

there is no switch case on python use if-else instead\_

### is & in

is - check are they really the same object, in - check is element in that data object or not

```py
  test = [1, 2, 3]
  test2 = [1, 2, 3]

  test is test2 # False
  1 in test # True
```

### For loop with else

else can added after loop so, it will do inside else after loop has been broken

```py
  for {condition}:
    # do stuff
  else:
    # do something
```

### Range

because there is no `for(i = 0; i < 10; i++)` in python range _accept only integer_

```py
  for element in range({number}):
    # do stuff

  for element in range({start}, {stop}, {step}):
    # do stuff
```

### While

loop as long as condition is _True_

### List and String

```py
  list = ['h', 'e']
  text = 'he'

  # can use with
  for c in {list|string}:
    print(c)

  # helper to know method able to use with
  help({variable})
```

string does not support index assignment but list can

### Format

control the looks of print

```py
  print('string: ' + {string} + 'int: ' + {int})

  # unable to assign but need to casting as string first

  'string: {} int: {}'.format('hello', 5)
  # able to assign value

  # can assign argument by index by
  ...format('hello', 5)
  # if reference {0} means 'hello'

  # named argument
  ...format(h='hello')
  # ref {h} means 'hello'

  # number
  {:>3.5f}...format(1.23)
  > means step space
  # [][][]1.23000
```

ref: [pyformat](https://pyformat.info/)
_For python 3.6+_

```py
  f'string: {a} int: {b}'
```

### Escape String

can be use "'" double quote or '\'' backslash

ref: [string-doc](https://docs.python.org/2.0/ref/strings.html)

### DS-List

Mutable, one type `['x', 'y']`

```py
  # iteration example
  for element in list:
    new_list.append(element)

  new_list = [el for el in list] # the result will be the same

  new_list = [el for el in list if el % 2 == 0] # added if
```

### Set

Immutable, unorderered, no duplicate, one type `{'x', 'y'}`

```py
  test_set = set('xyz') # {'x', 'y', 'z'}
  test_set2 = set(['xyz', 'abc']) # {'xyz', 'abc'}
```

### Tuple

Immutable, ordered, duplicated, multiple type `('x', 'y')`

### Dictionary

Mutable. unordered, no duplicate key like `json object`

```py
  test = [('a': 1), ('b': 2)]
  # make a list to dictionary
  dict_test = {key: value for (key, value) in test}
```

### Enumerate

if in for loop it will return index and data of iteration

```py
  for (index, data) in enumerate(list):
    ... do stuff
```

### Copiled other complex type

`the basic type` can coplied because it reference by value but `the complex type` reference by address (pass by reference) like pointer

```py
  list = [A, B, C]
  copied = list
  copied = copied.append(Z)
  # list = [A, B, C, Z]
  # copied = [A, B, C, Z]

  right_one = list[:] # copied all list - range selector
  right_one = right_one.append(X)
  # right_one = [A, B, C, X]
  # list = [A, B, C, Z]
  # copied = [A, B, C, Z]

  # list [start:end] # print start to end - 1
  # list [:-1] # print start to len(list) - 1

  # note: it works with tuple as well (tuple = (1,2,3,4))
  # sets (sets = {1,2,3,4}) does not work
```

### Shallow vs deep copies

`list[:]` this is shallow copy bacause for the complex list like array of dictionary will not full copied

**Note:** the inner data structures cannot copied

### is and ==

`==` will check only value but `is` will check in address level if the same that means it is the same object

**Note:** Trying by using data like list

**Additional:** [dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)

### All and Any

By example or think it like `AND, OR`

```py
  any([True, False, False]) # return True
  all([True, False, False]) # return False

  # Application
  list = [-1, 2, 3, 4]
  all([n > 0 for n in list])
```

### Comparison between data structures (python)

| type/test  |           list-comprehension ex. [e for e in set]           | iteration | indexing |      unpacking ex. a,b = list      |
| :--------: | :---------------------------------------------------------: | :-------: | :------: | :--------------------------------: |
|    list    |                              Y                              |     Y     |    Y     | Y (if unpack all element in there) |
|    set     |                              Y                              |     Y     |    N     | Y (if unpack all element in there) |
|   tuple    |                              Y                              |     Y     |    Y     | Y (if unpack all element in there) |
| dictionary | Y (with items and while iterate need to use (index, value)) |     Y     |    Y     |        Y (return only keys)        |

### List comprehension

Use `map()` to iterate list with do something with it by function

```py
  map({function}, {variable})

  def mul(e):
    return e*2

  list = [1,2,3]
  list(map(mul, list)) # 2,4,6

  # if does not use list casting it will return obj address
```

### Lambda function

Relate with above lecture section

```py
  list(map(lamda el: el * 2, list))

  # after lambda declaration will be return data
```

### Reducing list

Such as 1,2,3,4,5,6 => 21

### Import

`import {package_name}`

### Unpack argument of function

Single `*` multiple argument, Double `**` dictionary aka. keyword_arguments

```py
  def x(*args):
    print(args)

  # Turn argument to many function arguments
  "Test {} {} {}".format(*[1,2,3]) # Test 1 2 3

  def test(*args, **kwargs):
    for k, arg in kwargs.items():
      print(k, arg)
```

### Importing

Use keyword `import <package_name>` can call with `<package_name>.method`

Or using alias `import <package_name> as <name>` call by `<name>.method`

Or import only selected feature like `from <package> import <feature_name>`

`from <package_name> import something<*>` but not recomended because it might override some feature that imported

### Handling File Access

```python
# Life cycle
open(name, mode) # r: read, w: write, r+: read & write, x: write failed if file exist, a: append, b: binary mode

# f = open('demo.txt', mode='r')
# f.write('Hello from Python!\n')
# f.close() # Program will finished file written but does not finished

# f.write('Hello from Python!\n')
# f.write('Hello from Python!\n')
# f.write('Hello from Python!\n')
# f.write('Hello from Python!\n')
# f.close()

# From this line program will not create demo.txt with content
# Due to program does not finished yet
# user_input = input('Please enter input: ')


# Wrong mode make error
# Wrong mode can erase file content: w while read file
# file_content = f.read()
# f.close()
# print('file content is: {}'.format(file_content))

# file_content = f.readlines()
# f.close()
# Return as list
# print('file content is: {}'.format(file_content))

# for line in file_content:
#     # Remove special charactor
#     print(line[:-1])

# Like
# line = f.readline()
# print(line[:-1])
# print(line[:-1])
# print(line[:-1])
# print(line[:-1])
# print(line[:-1])
# line = f.readline()
# while line:
#     print(line)
#     line = f.readline()
# f.close()

# with statement for blocking code
with open('demo.txt', mode='w') as f:
    # line = f.readline()
    # while line:
    #     print(line)
    #     line = f.readline()
    # f.close()
    f.write('Test blocking')
    # Blocking will close file automatically
user_input = input('Testing:')
print('done!')
```

### Instead of JSON change to Binary

use pickle and other method like json

### Pickle vs JSON

Pickle works for all python type, binary format
JSON works only json, convert data to text

### Debugger

in vscode we need to create JSON on launch.json. You can review the variable by run debugger

### Try-except

python is a code block so it can catch an error block by block

```python
  try:
    # line of code
  except (TYPE1, TYPE2):
    # handling
  except TYPE1:
    # handling
  except: # All error catch should be not great idea
    # other error does not match type will comes here
  finally:
    # even though error or not will come here
```

### Which one should handle

Only unpredictable should handle such IOError, OSError

### OOP

Treat procedural as class and object with using method

- Class is like a blueprint
- Object created by class we can call it is instance

Example OOP

```python
  class Car:
  # Class attributes
  # top_speed = 100
  # warnings = []

  # constructor
  def __init__(self, s_top_speed=100):
      super().__init__()
      # attribute of instance
      # public
      self.top_speed = s_top_speed
      # private
      self.__warnings = []

  def __repr__(self):
      print('Printing...')
      return 'Top speed: {}, Warnings: {}'.format(self.top_speed, len(self.__warnings))

  def add_warning(self, warning_text):
      self.__warnings.append(warning_text)

  def get_warning(self):
      return self.__warnings

  # Self represent instance of the class
  def drive(self):
      print('Broonnnnnnnnnnnnnnnn {} kph'.format(self.top_speed))

  car1 = Car()
  car1.drive()
  # car1.warnings.append('Warnings')
  car1.add_warning('Warnings')
  # print(car1.__warnings) # Cannot called from outside
  # print(car1.__dict__)  # Print attribute as dictionary
  # print(car1.top_speed.__str__())  # String output
  # print(car1.__repr__())  # General output
  print(car1)  # General output like above
  print(car1.get_warning())

  print('#########')
  # Directly attach the class, Should not do
  # Need to make it effect only an instance
  # Car.top_speed = 200
  # car1.warnings.append('Warnings')

  car2 = Car(200)
  car2.drive()
  # print(car2.__warnings)
  # print(car2.__dict__)  # Print attribute as dictionary
  print(car2.get_warning())

```

#### VS Dict

Can hold data as object, not based on blueprint

#### Why need OOP

Structured and created quickly, Also include method not just a field and allow to write clean code

### OOP example with inheritance

```python
############### Vehicle.py

class Vehicle:
  # Class attributes
  # top_speed = 100
  # warnings = []

  # constructor
  def __init__(self, s_top_speed=100):
      super().__init__()
      # attribute of instance
      # public
      self.top_speed = s_top_speed
      # private
      self.__warnings = []

  def __repr__(self):
      print('Printing...')
      return 'Top speed: {}, Warnings: {}'.format(self.top_speed, len(self.__warnings))

  def add_warning(self, warning_text):
      self.__warnings.append(warning_text)

  def get_warning(self):
      return self.__warnings

  # Self represent instance of the class
  def drive(self):
      print('Broonnnnnnnnnnnnnnnn {} kph'.format(self.top_speed))

############### Car.py

from vehicle import Vehicle

class Car(Vehicle):
    def __init__(self, s_top_speed=100): # Access to the base class
      super().__init__(s_top_speed) # Auto add variable into other class

    def print_looks(self):
        print('Looks what the nice car is..')

car1 = Car()
car1.drive()

# car1.warnings.append('Warnings')

car1.add_warning('Warnings')

# print(car1.\_\_warnings) # Cannot called from outside

# print(car1.**dict**) # Print attribute as dictionary

# print(car1.top_speed.**str**()) # String output

# print(car1.**repr**()) # General output

print(car1) # General output like above
print(car1.get_warning())

print('#########')

# Directly attach the class, Should not do

# Need to make it effect only an instance

# Car.top_speed = 200

# car1.warnings.append('Warnings')

car2 = Car(200)
car2.drive()

# print(car2.\_\_warnings)

# print(car2.**dict**) # Print attribute as dictionary

print(car2.get_warning())

############### Bus.py

from vehicle import Vehicle

class Bus(Vehicle):
    def __init__(self, s_top_speed=100):
        super().__init__(s_top_speed)

          # attribute of instance
          # public
          self.top_speed = s_top_speed
          # private
          self.__warnings = []
          self.passengers = []

    def add_group(self, passenger):
        self.passengers.append(passenger)

bus1 = Bus(80)
bus1.add_group(['A', 'B', 'C'])
print(bus1.passengers)

```

### Instance vs Class vs Static methods & attibutes

Instance: like before section
Class: no new object instance, follow example

```python
  class Test:
    result = 1
    @classmethod # Decorator - use for change behavior or something | need to access something from the class
    def add(cls, a): # Need cls instead of self
      return cls.result + a

  Test.add(3) # return 4
```

Static: cannot access method from inside

```python
  class Test:
    result = 1 # cannot access method from inside
    @staticmethod # Decorator | works only input gets in no change class in big picture
    def add(a): # No self needed
      return a

  Test.add(3) # return 3
```

### Private attribute

Just add `__` in front of variable like `self.__blockchain`

Need getter function for calling from outside class

```py
### A.py
class A:
  def __init__(self):
    self.__private_attr = "test_attr"

  def get_private_attr(self):
    return self.__private_attr

### B.py
from A import A

print(A.get_private_attr())
```

### Attribute vs Properties

**Attribute:** Variable that attached into a class

```py
class A:
  result = 5

  def __init__(self):
    self.name = 'Test' # This is an attribute
```

**Properties:**

Can define logic freely

```py
class B:
  def __init__(self):
    self.name = 'Test'

  @property # getter | return copy of __name # property
  def name(self):
    return self.__name

  @name.setter # setter # property
  def name(self, val):
    self.__name = val
```

### The Modules

When need to separate source into its folder. Let's getting knows `Modules`

```bash
├── blockchain.py
├── block.py
├── node.py
├── README.md
├── transaction.py
└── utils
    ├── hashutil.py
    ├── __init__.py
    ├── printable.py
    └── verification.py
```

Such `utils` folder. To make it know: add `__init__.py`

### pycache

It help to compile the code faster. Any change it will recompiled and store in `__pycache__`

### Controlling exports

In python, nothing private

- `_variable` to tell python not to import it when use `import \*`
- `__all__` to control exports when use `import \*`

```py
# try to import
import utils.hash_util
dir(utils.hash_util)
# ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'hash_block', 'hl', 'hs256', 'json']

__all__ = ['hash_block', 'hl', 'hs256'] # Will not found json when
# from utils.hash_util import *
```

Apply this into `__init__.py`

```py
from utils.hashutil import hs256

__all__ = ['hs256']

# When
# from utils import *
# Will got only hs256
```

### Special variable **name**

`__name__` -> When add into dir that run file will return `__main__`, When add to other file will return `filename`

```py
# This will help when this file can be import somewhere and reuse for import also
if __name__ == '__main__':
    node = Node()
    node.listen_for_input()
```
