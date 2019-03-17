# chartreux

`chartreux` is a templating engine for Python with emphasis on simplicity.

```python

import chartreux

template = '''
    @if lang == 'en'
        Hello, {name}!
    @elif lang == 'fr'
        Bonjour, {name}!
    @end
'''

context = {
    'name': 'User',
    'lang': 'en',
}

print(chartreux.render_text(template, context))
```

 * [API](#api)
     * [options](#options)
 * [language syntax](#language-syntax)
     * [expressions](#expressions)
     * [interpolations](#interpolations)
     * [commands](#commands)
 * [built-in commands](#built-in-commands)
     * [let](#let)
     * [var](#var)
     * [if](#if)
     * [each](#each)
     * [with](#with)
     * [def](#def)
     * [block](#block)
     * [code](#code)
     * [quote](#quote)
     * [include](#include)
     * [option](#option)
 * [built-in filters](#built-in-filters)
 * [info](#info)

## API

`chartreux` templates are compiled to python functions, which return the rendered text when called. Compilation is reasonably fast, but it's also possible to obtain a compiled function, cache it and call it directly later on. 

```
chartreux.render_text(text: str, context: dict, **options) -> str         
```

Compiles a template text and renders it.

```
chartreux.render_path(path: str, context: dict, **options)  -> str        
```

Compiles a template from the path and renders it.

```
chartreux.render(template: callable, context: dict, **options) -> str 
```

Renders a compiled template (function).

```
chartreux.compile(text: str, **options) -> callable         
```

Compiles a template and returns a function (suitable for `render`).

```
chartreux.translate(text: str, **options) -> str         
```

Compiles a template into python source code.


### options

Compile-time options affect how templates are compiled:


option|value|default
------|----|----
`filter` | default filter (added to every interpolation unless it already has a filter) | `None`
`globals` | list of names to be treated as global in the template | `[]`
`name` | name for the compiled function | `'render'`
`path` | template path | `''`
`silent` | activate the silent mode. In the silent mode, possible exceptions (e.g. undefined variables) are not raised, but passed to a `warn` function, if provided, and swallowed otherwise | `False`

Run-time options are passed to compiled template functions:

option|value|default
------|----|----
`runtime` | runtime class (NB: not an object) | `chartreux.Runtime`
`warn` | a function that accepts a string (an error message) | `None`

## language syntax

The `chartreux` input, or "flow", consists of plain text, interpolated expressions, enclosed in `{}` and commands, which start with a `@` by default.

The flow is line-oriented (like python), however, indentation doesn't matter.

### expressions

`chartreux` expressions are just python expressions and can include:

- string, number and list literals
- subscripts and slices
- arithmetic, boolean and comparison operators
- function calls

Expressions can reference context variables (passed to a template in the `context` dict), locals (defined in the template) and globals (python built-ins and `globals`). 

Dot syntax (`object.prop`) can be used to refer to an object attribute or a dict key. This applies to context and local variables, but not to globals.

An expression can be followed by one or multiple filters, separated by a `|`. A filter can be

- a name of a filter function (built-in or local). The expression is passed as an argument to the function. 
- a function call. The expression is injected as a first argument.
- a string, which is interpreted as python `format` code 

### interpolations

Interpolations are expressions enclosed in `{}` and must start with a non-whitespace, so when you need a literal curly brace, make sure it's followed by a newline or a space (which is normally the case for C-alike languages or CSS).

###### example:
```
{
    this won't be parsed
}

{person.name} 
{race | upper} 
Active for {active} years ({active * 365} days)
{roles | sort | join('/')}
{credits | ':.2f'} cr.
```
###### context:
```
{
    'person': {'name': 'Benjamin'},
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

Benjamin 
HUMAN 
Active for 7 years (2555 days)
captain/emissary/father
1500.00 cr.
```

You can specify a default filter (`filter` option) for the template. The default filter will be added to all iterpolations, unless they already have a filter. 

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
```

or a block form:

```
@let varName
    flow
@end
```

In the second case, the value of the variable will be the intepolated "flow":


###### example:
```
@let number = 5
@let race = 'klingon'

@let message
{number} {race} ships approaching
@end

The message was: {message}
```
###### result:
```
The message was: 5 klingon ships approaching
```

### var

Declares one or multiple variables as local without giving them a value. Used in combination with `@code` blocks to inject names in the template scope:

###### example:
```
@var info, full_version

@code 
    import sys
    info = sys.version_info
    full_version = sys.version
@end

This is python {info[0]}, specifically {full_version}
```
###### result:
```
This is python 3, specifically 3.6.5 (default, Mar 30 2018, 06:42:10) 
[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.39.2)]
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
        {'user': {'anonym': True}}
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
@def name arguments
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

12^2 = {square(12)}
```
###### result:
```
12^2 = 144
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

- as a filter (with or without arguments)

###### example:
```
@def boldify x
    @return x | '<b>{}</b>' 
@end

very {'important' | boldify} stuff

@def repeat(a, b)
    @return a * b
@end

{'!' | repeat(10)}
```
###### result:
```
very <b>important</b> stuff


!!!!!!!!!!
``` 


### block

Defines a "block" function. Block functions are similar to `def` functions, but can be used as block commands. The flow of the block command will passed as a first argument to the function: 


###### example:
```
@block box(flow, class_name)
<div class="{class_name}">{flow}</div>
@end

@box 'green'
<h1>Hello,</h1>
<h2>Dax</h2>
@end
```
###### result:
```
<div class="green"><h1>Hello,</h1>
<h2>Dax</h2>
</div>
``` 

### code

Inserts raw python code. Can have a line or a block form. The indentation doesn't have to match the outer level, but has to be consistent within a block. `print` emits the content to the template output.

###### example:
```
@code print(2+2)

@code
    import sys
    print(sys.version)
@end
```
###### result:
```
4
3.6.5 (default, Mar 30 2018, 06:42:10) 
[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.39.2)]
``` 

### quote

`@quote name` stops parsing until `@end name` is encountered.


###### example:
```
Try this:

@quote ex1
    @if expression
        {variable}
    @end
@end ex1
```
###### result:
```
Try this:

    @if expression
        {variable}
    @end
```

### include

Includes another template. The path argument is relative to the current template path:


```
@include ./other-template.cx
```

### option

Sets an compile-time option for this template (see "options"):

```
@option filter html

```

## built-in filters

`chartreux` comes with a few useful built-in filters:

###### example:
```
html    : {'<b>hi</b>' | html} or {'<b>hi</b>' | h}
unhtml  : {'&lt;b&gt;' | unhtml}
nl2br   : {'one\ntwo\nthree' | nl2br}
strip   : {'  xyz ' | strip}>
upper   : {'hello' | upper}
lower   : {'HELLO' | lower}
linkify : {'see http://google.com' | linkify(target='_blank')}
cut     : {'yoknapatawpha' | cut(3, ellipsis='...')}
json    : {'füßchen' | json}
slice   : {'abcdef' | slice(1, 3)}
join    : {[1, 2, 3] | join(':')}

split: 

    @each '1/2/3' | split('/') as x
        >{x}
    @end

lines:
    
    @each 'one\ntwo\nthree' | lines as x
        >{x}
    @end
```
###### result:
```
html    : &lt;b&gt;hi&lt;/b&gt; or &lt;b&gt;hi&lt;/b&gt;
unhtml  : <b>
nl2br   : one<br/>two<br/>three
strip   : xyz>
upper   : HELLO
lower   : hello
linkify : see <a href="http://google.com" target="_blank" rel="noopener noreferrer">http://google.com</a>
cut     : yok...
json    : "f\u00fc\u00dfchen"
slice   : bc
join    : 1:2:3

split: 

        >1
        >2
        >3

lines:
    
        >one
        >two
        >three
```

To add a new built-in filter, extend `chartreux.Runtime` and define a static function like 

```
filter_<filter-name>(cls, value, ...more args)
```

Then, pass your class as `runtime=` to a `render...` function:

```
class MyRuntime(chartreux.Runtime):
    @classmethod
    def filter_ljust(cls, value, width):
        return str(value).ljust(width)
...

my_template = '... {some_val | ljust(30)} ...'

chartreux.render_text(my_template, runtime=MyRuntime)
```

## info

(c) 2019 Georg Barikin (https://github.com/gebrkn). MIT license.
