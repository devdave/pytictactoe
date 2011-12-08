Barring time constraints, I did not implement a reference Tic Tac Toe application for
prudence.  Instead, the included sub-directory stickstick is a reference example
provided by the Prudence project.

Briefly, stick stick is an Ajax enabled note recording appliance backed by a
sqlalchemy managed Java H2 database.

Rudimentary tests showed the response time under siege for a NO-OP page/resource
was between 0.01 and 0.2 ms.

Memory profiling showed no obvious memory leaks under duress
Max resident was 279Mb on a 64Bit Ubuntu 11 environment
Max virtual was 599Mb