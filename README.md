<pre>
oooooooooool,;oooooooooool::ollooooooooo
ooooooooooooc;cooooooooooc;lollooooooooo
ooooooooooooo:;lool:;:lol,,loooooooooooo
oooooooooooooc':oo:...;oc,;ooooooooooooo
oooooooooooooo;,lo:...,oc;cooooooooooooo
ooooooooooooool;:o:...,l:;looooooooooooo
oooooooooooooooc;c:...'c;:oooooooooooooo
ooooooooollllooo:;,....,;coooooooooooool
oooooool:;::::ccl;......;llcc:::cooooool
oooooooolcloolc::;,'....,;,,,,,'':oooooc
ooooooolc:;::::::,;ldo:..,::::::,,:loolc
oooool:;;;:cllllc,',:;'.',;coolcll:;:ccc
oool:::loooooooc,::,',,';c:,;:cloool:,;c
ol:;:looooolll:,coollooloool;':ooooooc,;
l;;loollllllc,':ooooooooooooo:;coooooc::
l:cllllllooo:,:ooooooooooooooo:;looollc:
l::clooooool;;ooooooooooooooool;;loolccc
llcclooooool:coooooooooooooooooc,:oolccc
oooolooooool;:oooooooooooooooooo;';;::,,
oooooooooooc,:ooooooooooooooooooc,,,....
</pre>
# Pequeña Araña - A Humble Social Graph Tool
Pequeña Araña ("Little Spider") is a little application that was born from a desire to keep track of new connections at a large consulting firm. The use case was typically: "Who do I know that is an expert in FOO?". Originally, I created a simple schema and began entering nodes and edges manually in the [Gephi](https://gephi.org/) interface. This quickly became a bit awkward, as I needed to add several edges (and potentially nodes) for each new individual. Gephi's graph visualization and search capabilities are excellent, however, so I wanted to preserve the ability for it to read my professional graphs.

## Usage
To call the tool, ensure that you have installed the required modules via use of the requirements.txt. In particular, Pequeña Araña requires *networkx* and *npyscreen*. The curses-based front-end can be called with:

`$ python console-app.py`

from the project directory. This should display a main menu with options to create a graph, load a graph, etc.

![image](https://github.com/andrew-gearhart/pequena-arana/assets/2237295/8bfbcb1d-22d1-4fff-84e7-38d063821713)


Graphs can be loaded and exported into [GraphML](http://graphml.graphdrawing.org/) format, which is compatible with Gephi. A graph (either created new or loaded from a file) is only saved to a file upon an explicit save, altough the tool has the ability to warn you if you are planning a destructive action (except for the *Clear Graph* option, this happens immediately). Loaded graphs must adhere to the expected graph schema to ensure correct functioning--programmic creation of such graphs can be assisted via use of the included *connection_graph* module.

## Schema
At its core, Prequeña Araña is a small Python library that implements a simple professional graph schema with four types of nodes: *PERSON*, *ORGANIZATION*, *PLACE*, and *ACCOUNT*. There are currently only three types of edges:
* **ASSOCWITH**(PERSON, ORGANIZATION) - An individual was once or is a member of a particular organization
* **BASEDIN**(PERSON, PLACE) - A person has lived in a particular locaion
* **ONACCOUNT**(PERSON, ACCOUNT) - A person has been involved with a particular client account.

Node and edge types are differentiated by the *kind* attribute, and *PERSON* nodes include *skills* and *notes* attributes. These latter attributes are expected to be in a CSV format, but this is only currently relevant for *skills* due to the implementation of the search functionality. The schema rules are enforces loosely and irregularly--they can likely be broken easily, and I haven't put much effort into enforcement.
By default, Gephi will display the *label* for nodes and edges. So, I've duplicated *kind* in *label* for both of these objects. It's a little awkward. One can search for PERSON nodes based on matches with the PERSON's skills attribute. This search isn't case-sensitive, but other than that it requires an exact match.

## Limitations and Future Directions
The interface was developed using the [npyscreen](https://github.com/npcole/npyscreen) library, which is an ncurses-based library. After getting halfway through developing the interface, I realized that npyscreen hasn't been updated in a while--so I suspect that the library will eventually break and I'll need to re-implement the tool with another library. For the moment, however, it accomplishes its task.

A drawback of this library is that the search functionality is currently quite limited and doesn´t take great advantage of some of the features of npyscreen. I'm hoping to work on this in the near future, and potentially add skills matching based on partial or misspelled matches. I'd also like to order results based on the relative match of all skills associated with a PERSON, perhaps via embeddings such as [Word2vec](https://en.wikipedia.org/wiki/Word2vec).

#### Image Attribution
The image used to create the project ASCII art was "Spider meal" by Thomas Won is licensed under CC BY 2.0. To view a copy of this license, visit https://creativecommons.org/licenses/by/2.0/?ref=openverse. The image was converted to ASCII via the [ASCII Art Generator](https://www.ascii-art-generator.org/).
