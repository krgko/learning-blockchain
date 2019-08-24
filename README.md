# Learning blockchain

This project all about learning blockchain with consensus algorithm PoW (Proof of Work)

**If we understand this we will able to develop blockchain with any language**

## Requirement

1. Python

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
- **Hash:** use for reference block like an id. it stored on header of block(previous hase, current hash) - **Why hash needed in blockchain**: if need to verify using previous transaction as chain there are many transactions and it very long so hashing can help to represent data to strings for using in verify step 
- **Nonce (Number Used Once):** use for prevent replay request for PoW it used to check validity for miner who won puzzle solving as well
- **Merkle Tree (data structure)** - use to check correctly of transaction in block and make sure that does not modified (a.k.a checksum) - some blockchain generate hash from merkle root
- **Data structure** - maybe key-store, ...

- **Maniplate the chain** the blockchain does not allow to modify some data on the chain and the chain will invalid
- **Blockchain verification** It use hash that calculate each block this will ensure that chain cannot manipulated
- **To verify block hashes** Can check by try to create another set of hash as current_hash and reconcile with previous_hash

## Proof of work
Mining is challenging -> for security and control amount of coins
- Find a number which fullfill PoW requirement (Answer of puzzle)
- Take block data into account -> **If number is correct will added to block metadata then commit with transaction and previous hash**
- Other node can verify PoW easily

**Process**
- Transactions - difference from Nonce
- Previous hash
- Proof (Nonce: Number used once) - increment in loop 0, ... n
Checking PoW by hash all above into a hash e.g `00[a-f0-9]{62}` 00 is difficulty - miner need to find a correct hash

**Cheating**
Add old block -> check hash will failed to matched with previous hash
Nonce changed -> that is a part of hash all of hashes after cheated block will change and PoW takes time so, all the block will be recalculated (These step will occur with block has been validated)

## Important note

- Python code indentation is the most significant. developers need to care about

## New things learned from python

- **Variable:** assign variable python has no data type(weak type)
  ```
    variable = 'string' # string
    variable = 1        # int
    variable = 1.2      # float
    variable = True     # boolean
  ```
- **Casting:** make current type to target type
  ```
    int(12), str(12) # type string
  ```
- **Number-operation**
  ```
    +, - , * , /
    ** - power
    // - divide with floor
    % - modulo
  ```
  **Note:** +, \* can be worked with string to concatenate or iterate
- **Weird behavior of python number** - if number cannot divide that got finite degit and do operation like `1-0.9 the answer will be 0.0999999998`
- **List:** or array on other programming language

  ```
    list.append() - append element to list
    list.remove(index) - remove with index
    list.pop() - pop element from list

    # accessing last element in list for python
    # list[-1]
  ```

- **Function:** wrapper of codes for calling more than once
  ```
    def function_name():
        ...
        return {something}
  ```
- **Default argument**
  ```
    def function_name(variable1='something_any_type'):
        ...
  ```
- **Variable scope:** contains with 2 types are global and local

  ```
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

- **comment for document:** create comment by use """(triple double quotes)
- **loop:** python contains for loop and while loop

  ```
    # iterate through elements list
    for elem in list:
      ...

    # repeat code until true
    while True:
      ...
  ```

- **if-else:** condition like other language
  ```
    if condition:
      ...
    elif condition:
      ...
    else:
      ...
  ```
- **continue-break:** this keyward will be in for-loop or while loop

  ```
    # end current iterate and continue iteration
    continue

    # end loop
    break
  ```

- **not:** use for check in negative case work only string case
  ```
    if char not in str:
      ...
  ```
- **and,or:** use for join condition, the result can check from truty table
  ```
    condition_1 and condition_2
    condition_1 or condition_2
  ```
- **grouping conditions:** conditions can be combined to check like
  ```
    (condition_1 {logic} condition_2) {logic} condition_3
  ```
- **switch case:** *there is no switch case on python use if-else instead*
- **is & in:** is - check are they really the same object, in - check is element in that data object or not
  ```
    test = [1, 2, 3]
    test2 = [1, 2, 3]
    
    test is test2 # False
    1 in test # True
  ```
- **For loop with else** else can added after loop so, it will do inside else after loop has been broken
  ```
    for {condition}:
      # do stuff
    else:
      # do something
  ```
- **Range** because there is no `for(i = 0; i < 10; i++)` in python range *accept only integer*
  ```
    for element in range({number}):
      # do stuff

    for element in range({start}, {stop}, {step}):
      # do stuff
  ```
- **While** loop as long as condition is *True*
- **List and String**
  ```
    list = ['h', 'e']
    text = 'he'

    # can use with
    for c in {list|string}:
      print(c)
    
    # helper to know method able to use with
    help({variable}) 
  ```
string does not support index assignment but list can
- **Format** control the looks of print
  ```
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
ref: https://pyformat.info/
*For python 3.6+*
  ```
    f'string: {a} int: {b}'
  ```
- **Escape String** can be use "'" double quote or '\'' backslash
ref: https://docs.python.org/2.0/ref/strings.html
- **List** Mutable, one type `['x', 'y']`
  ```
    # iteration example
    for element in list:
      new_list.append(element)

    new_list = [el for el in list] # the result will be the same

    new_list = [el for el in list if el % 2 == 0] # added if
  ```
- **Set** Immutable, unorderered, no duplicate, one type `{'x', 'y'}`
  ```
    test_set = set('xyz') # {'x', 'y', 'z'}
    test_set2 = set(['xyz', 'abc']) # {'xyz', 'abc'}
  ```
- **Tuple** Immutable, ordered, duplicated, multiple type `('x', 'y')`
- **Dictionary** Mutable. unordered, no duplicate key like `json object`
  ```
    test = [('a': 1), ('b': 2)]
    # make a list to dictionary
    dict_test = {key: value for (key, value) in test}
  ```
- **Enumerate** if in for loop it will return index and data of iteration
  ```
    for (index, data) in enumerate(list):
      ... do stuff
  ```
- **Copiled other complex type** `the basic type` can coplied because it reference by value but `the complex type` reference by address (pass by reference) like pointer
```
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
- **Shallow vs deep copies** `list[:]` this is shallow copy bacause for the complex list like array of dictionary will not full copied
Note: the inner data structures cannot copied
- **is and ==** `==` will check only value but `is` will check in address level if the same that means it is the same object
**Note:** Trying by using data like list

**Additional:** https://docs.python.org/3/tutorial/datastructures.html#dictionaries
- **All and Any** By example or think it like `AND, OR`
```
  any([True, False, False]) # return True
  all([True, False, False]) # return False

  # Application
  list = [-1, 2, 3, 4]
  all([n > 0 for n in list])
```
- **Comparison between data structures**

|  type/test |           list-comprehension ex. [e for e in set]           | iteration | indexing |      unpacking ex. a,b = list      |
|:----------:|:-----------------------------------------------------------:|:---------:|:--------:|:----------------------------------:|
|    list    |                              Y                              |     Y     |     Y    | Y (if unpack all element in there) |
|     set    |                              Y                              |     Y     |     N    | Y (if unpack all element in there) |
|    tuple   |                              Y                              |     Y     |     Y    | Y (if unpack all element in there) |
| dictionary | Y (with items and while iterate need to use (index, value)) |     Y     |     Y    |        Y (return only keys)        |
- **List comprehension**
Use `map()` to iterate list with do something with it by function
```
  map({function}, {variable})

  def mul(e): 
    return e*2

  list = [1,2,3]
  list(map(mul, list)) # 2,4,6

  # if does not use list casting it will return obj address
```
- **Lambda function**
For above lecture section
```
  list(map(lamda el: el * 2, list))

  # after lambda declaration will be return data
```
- **Reducing list**
Such as 1,2,3,4,5,6 => 21
- **Import**
`import {package_name}`
- **Unpack argument of function**
Single `*` multiple argument, Double `**` dictionary aka. keyword_arguments
```
  def x(*args):
    print(args)
  
  # Turn argument to many function arguments
  "Test {} {} {}".format(*[1,2,3]) # Test 1 2 3

  def test(*args, **kwargs):
    for k, arg in kwargs.items():
      print(k, arg)
```
- **Importing**
Use keyword `import <package_name>` can call with `<package_name>.method`
Or using alias `import <package_name> as <name>` call by `<name>.method`
Or import only selected feature like `from <package> import <feature_name>`
`from <package_name> import *` but not recomended because it might override some feature that imported 