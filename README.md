# chartreux

`chartreux` is a templating/configuration language for Python with emphasis on simplicity.

```python

import chartreux

template = '''
    @each users as user
        @if lang == 'en'
            Hello, {user}!
        @elif lang == 'tlh'
            Qapla, {user}!
        @end
    @end
'''

context = {
    'lang': 'en',
    'users': ['Dax', 'Quark', 'Worf']
}

print(chartreux.render(template, context))
```

 * [API](#api)
     * [options](#options)
 * [language syntax](#language-syntax)
     * [comments](#comments)
     * [expressions](#expressions)
     * [interpolations](#interpolations)
     * [commands](#commands)
 * [built-in commands](#built-in-commands)
     * [let](#let)
     * [if](#if)
     * [each](#each)
     * [with](#with)
     * [def](#def)
     * [block](#block)
     * [return](#return)
     * [code](#code)
     * [import](#import)
     * [quote](#quote)
     * [comment](#comment)
     * [include](#include)
     * [option](#option)
 * [built-in filters](#built-in-filters)
 * [info](#info)

## API

`chartreux` templates are compiled to python functions. A function is supposed to be called with a `context` dict and return the rendered text. The compilation is reasonably fast, but it's also possible to obtain a compiled function, cache it and call it directly later on. 

Compile a template text and render it with the context:
```
chartreux.render(text: str, context: dict = None, **compile_and_runtime_options) -> str         
```

Compile a template from a file and render it with the context:
```
chartreux.render_path(path: str, context: dict = None, **compile_and_runtime_options)  -> str        
```

Compile a template and return a function:
```
chartreux.compile(text: str, **compile_options) -> callable         
```

Compile a template from a file and return a function:
```
chartreux.compile_path(path: str, **compile_options) -> callable         
```

Compile a template into python source code:
```
chartreux.translate(text: str, **compile_options) -> str         
```

Invoke a compiled template  and render it with the context:
```
chartreux.call(tpl: callable, **runtime_options) -> str
```

### options

Compile-time options affect how templates are compiled:


option|    |default
------|----|----
`strip`   | strip leading/trailing whitespace from text blocks | `False`
`commands`| custom commands (plugin) object | `None`
`filter`  | default filter (added to every interpolation unless it already has a filter) | `None`
`finder`  | resolver for includes. Should be a function that receives `(base_path,include_path)` and returns an absolute path | `None`
`globals` | list of names to be treated as global in the template | `[]`
`name`    | name for the compiled function | `'_RENDER'`
`path`    | template path | `''`
`syntax`  | syntax options | `None`

The `syntax` option allows you to change `chartreux` syntax. It should be a dict with four regular expressions:

key|    |default
------|----|----
`command` | matches a command | `r'^\s*@(\w+)(.*)'`
`comment` | matches a comment | `r'^\s*##'`
`start`   | matches the interpolation start delimiter | `r'{(?=\S)'`
`end`     | matches the interpolation end delimiter | `r'}'`

Run-time options are passed to compiled template functions:

option|    |default
------|----|----
`runtime` | runtime object | `chartreux.Runtime()`
`error` | a function that accepts three arguments: an exception, a source template path, and a line number. If provided, run-time errors are passed to this function | `None`


## language syntax

The `chartreux` input, or "flow", consists of plain text, interpolated expressions, enclosed in `{}` and commands, which start with a `@` by default.

The flow is line-oriented (like python), however, indentation doesn't matter.


### comments

Lines starting with `##` are considered comments and ignored:

###### example:
```
##my test
hello
```
###### result:
```
hello
```

### expressions

`chartreux` expressions are just python expressions and can include:

- string, number and list literals
- subscripts and slices
- arithmetic, boolean and comparison operators
- conditional operator
- function calls

Expressions can reference context variables (passed to a template in the `context` dict), locals (defined in the template) and globals (python built-ins and `globals`). 

Dot syntax (`object.prop`) can be used to refer to an object attribute or a dict key. This applies to context and local variables, but not to globals.

An expression can be followed by one or multiple filters, separated by a `|`. A filter can be

- a name of a filter function (built-in or local). The expression is passed as an argument to the function. 

```
{some_var | html}
```

- a function call. The expression is injected as a first argument.

```
{some_var | linkify(target='_blank')}
```

- a string, which is interpreted as python `format` code

```
{some_var | ':.2f'}
``` 

### interpolations

Interpolations are expressions enclosed in `{}` and must start with a non-whitespace, so when you need a literal curly brace, make sure it's followed by a newline or a space (which is normally the case for C-alike languages or CSS).

###### example:
```
{
    this won't be parsed
}

{name.last},  {name.first}
{race | upper}
Active for {active} years ({active * 365} days)
{roles | sort | join('/')}
{credits | ':.2f'} cr.
```
###### context:
```
{
    'name': {'first': 'Benjamin', 'last': 'Sisko'},
    'race': 'human',
    'active': 7,
    'roles': ['father', 'captain', 'emissary'],
    'credits': 1500,
}
```
###### result:
```
{
    this won't be parsed
}

Sisko,  Benjamin
HUMAN
Active for 7 years (2555 days)
captain/emissary/father
1500.00 cr.
```

You can specify a default filter (`filter` option) for the template. The default filter will be added to all interpolations, unless they already have a filter.

### commands

Commands start with a `@keyword`, followed by one or multiple arguments. 

A line command acts until the end of line:

```
@let myVar = 5
```

A block command acts until the respective `@end`:

```
@let myVar
    some
    text
@end
```

Block commands can be nested:

```
@if ships
    @each ships as ship
        @if ship.size > 10
            big ship
        @else
            little ship
        @end
    @end
@end

```

## built-in commands

### let

Adds a new local variable. Can have a line form:

```
@let varName = expression
@let varName, varName1, ... = expression
```

(the equals sign is optional), or a block form:

```
@let varName
    flow
@end
```

In the second case, the value of the variable will be the interpolated "flow":

###### example:
```
@let number 5
@let race 'klingon'

@let message
{number} {race} ships approaching
@end

The message was: {message}
```
###### result:
```
The message was: 5 klingon ships approaching
```

### if

Conditional output. The syntax is

```
@if expression
    flow
@elif expression
    flow
@elif expression
    flow
@else
    flow
@end
```

`elif` and `else` blocks are optional.

###### example:
```
@if race == 'human'
    Hello
@elif race == 'klingon'
    Qapla
@end
```
###### context:
```
{'race': 'klingon'}
```
###### result:
```
    Qapla
```

### each

Loop construct. You can iterate list and dict expressions:

```
@each expression as value

@each expression as key, value
```

An optional `index` clause adds variables for the current index and the overall length. An optional `else` block is rendered for empty expressions:

###### example:
```
@each people | sort as name index n, total
    Member {n} of {total}: {name}
@end
    
@each locations as name, location index n
    {n}. {name} is in the {location}
@end
    
@each items as item
    {item}
@else
    No items!
@end
```
###### context:
```
{
    'people': ['Julian', 'Quark', 'Dax'],
    'locations': {
        'Dax': 'ops',
        'Julian': 'infirmary',
        'Quark': 'bar',
    },
    'items': [],
}
```
###### result:
```
    Member 1 of 3: Dax
    Member 2 of 3: Julian
    Member 3 of 3: Quark
    
    1. Dax is in the ops
    2. Julian is in the infirmary
    3. Quark is in the bar
    
    No items!
```

### with

Conditionally render a flow if an expression is not "empty" (undefined, whitespace-only string, empty list or dict). A complex expression can be aliased for brevity. An optional `else` block is rendered for empty expressions:


###### example:
```
@with environment[0].user.name as s
    Hello {s}
@end

@with environment[1].user.name as s
    Hello {s}
@end

@each ships as ship
    {ship.name}
    @with ship.weight as w
        weight {w}
    @else
        weight unknown
    @end
@end
```
###### context:
```
{
    'environment': [
        {'user': {'name': 'Dax'}},
        {'user': {'anonymous': True}}
    ],
    'ships': [
        {'name': 'Defiant', 'weight': 1234},
        {'name': 'Valiant'},
    ]
}
```
###### result:
```
    Hello Dax


    Defiant
        weight 1234
    Valiant
        weight unknown
``` 

### def

Defines a function. The syntax is

```
@def name (arguments)
    flow
@end
```

Parentheses around arguments can be omitted. The result of the function will be its flow, unless there is an explicit `@return` command.

Once a function is defined, it can be called

- as an ordinary python function within an expression

###### example:
```
@def square n
    @return n * n
@end

12^2 + 3 = {square(12) + 3}
```
###### result:
```
12^2 + 3 = 147
```

- as a line command

###### example:
```
@def banner text, sym='*'
    {sym * 3} {text} {sym * 3}
@end

@banner 'Hello'
@banner 'Hello', sym='!'
```
###### result:
```
    *** Hello ***
    !!! Hello !!!
```

- as a simple filter

###### example:
```
@def bold x
    @return x | '<b>{}</b>' 
@end

very {'important' | bold} stuff
```
###### result:
```
very <b>important</b> stuff
```

- as a filter with arguments

###### example:
```
@def repeat(arg, count)
    {arg * count}
@end

{'!' | repeat(10)}
```
###### result:
```
    !!!!!!!!!!
``` 

### block

Defines a "block" function. Block functions are similar to `def` functions, but can be used as block commands. The flow of the block command will passed as a first argument to the function: 


###### example:
```
@block box(flow, class_name)
    <div class="{class_name}">
        {flow | strip}
    </div>
@end

@box 'green'
    <h1>Hello</h1>
@end
```
###### result:
```
    <div class="green">
        <h1>Hello</h1>
    </div>
``` 

### return

`@return expression` returns an expression as a result of a `def` or `block` function.

###### example:
```
@block upper(flow)
    @return flow.upper()
@end

@upper
    Attention citizens
@end
```
###### result:
```
    ATTENTION CITIZENS
``` 

If you return `None`, nothing will be rendered:

###### example:
```
@def div a, b
    Division:
    @if b == 0
        @return
    @end
    {a/b} 
@end

@div 200 100
@div 200 0
@div 500 100
```
###### result:
```
    Division:
    2.0 
    Division:
    5.0
``` 

### code

Inserts raw python code. Can have a line or a block form. The indentation doesn't have to match the outer level, but has to be consistent within a block. `print` emits the content to the template output. The `_CONTEXT` dict can be used to read and write context variables:

###### example:
```
@code
    a = _CONTEXT['first']
    b = _CONTEXT['second']
    if a > b:
        print(a, 'is bigger than', b)
    else:
        print(a, 'is no bigger than', b)
@end
```
###### context:
```
{'first': 'Quark', 'second': 'Rom' }
```
###### result:
```
Quark is no bigger than Rom
```

### import

`@import module, module...` imports python modules into the template function.

###### example:
```
@import sys

This is python {sys.version}
```
###### result:
```
This is python 3.7.5 (default, Nov  1 2019, 02:16:32) 
[Clang 11.0.0 (clang-1100.0.33.8)]
```

### quote

`@quote name` returns the unparsed flow until `@end name` is encountered. `name` can be omitted if there are no commands in the flow.


###### example:
```
Try this:

@quote example
    @if expression
        {variable}
    @end
@end example
```
###### result:
```
Try this:

    @if expression
        {variable}
    @end
```

### comment

`@comment name` ignores the flow until `@end name` is encountered. `name` can be omitted if there are no commands in the flow.


###### example:
```
Quark
Julian
@comment
    Jadzia
@end
Ezri
```
###### result:
```
Quark
Julian
Ezri
```

### include

`@include path` includes another template. The path argument is relative to the current template path:

```
@include ./other-template.cx
```

### option

Sets a compile-time option for this template (see "options"):

```
@option filter html
```

## built-in filters

`chartreux` comes with a few useful built-in filters:

###### example:
```
html:     {'<b>hi</b>' | html} or {'<b>hi</b>' | h}
unhtml:   {'&lt;b&gt;' | unhtml}
nl2br:    {'one\ntwo\nthree' | nl2br}
strip:    <{'  xyz ' | strip}>
upper:    {'hello' | upper}
lower:    {'HELLO' | lower}
linkify:  {'see http://google.com' | linkify(target='_blank')}
cut:      {'yoknapatawpha' | cut(3, ellipsis='...')}
json:     {'füßchen' | json}
slice:    {'abcdef' | slice(1, 3)}
join:     {[1, 2, 3] | join(':')}
split:    {'1/2/3' | split('/') | join('.')}
lines:    {'one\ntwo\nthree' | lines | join('-')}
```
###### result:
```
html:     &lt;b&gt;hi&lt;/b&gt; or &lt;b&gt;hi&lt;/b&gt;
unhtml:   <b>
nl2br:    one<br/>two<br/>three
strip:    <xyz>
upper:    HELLO
lower:    hello
linkify:  see <a href="http://google.com" target="_blank">http://google.com</a>
cut:      yok...
json:     "f\u00fc\u00dfchen"
slice:    bc
join:     1:2:3
split:    1.2.3
lines:    one-two-three
```


## info

(c) 2019 Georg Barikin (https://github.com/gebrkn). MIT license.
