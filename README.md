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
- **Blocks:** wrapper transaction(s) with header and append to chain
- **Blockchain:** multiple block that appended start from first block(genesis block) like chain (data structure like link-list)
- **Hash:** use for reference block like an id. it stored on header of block(previous hase, current hash)
- **Nonce (Number Used Once):** use for prevent replay request for PoW it used to check validity for miner who won puzzle solving as well
- **Merkle Tree (data structure)** - use to check correctly of transaction in block and make sure that does not modified (a.k.a checksum) - some blockchain generate hash from merkle root

- **Maniplate the chain** the blockchain does not allow to modify some data on the chain and the chain will invalid
- **Blockchain verification** It use hash that calculate each block this will ensure that chain cannot manipulated

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