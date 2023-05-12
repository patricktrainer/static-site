# Understanding C-Store: Columnar Databases and Data Intensive Analytics

Created: Apr 20, 2020 8:26 AM
URL: https://medium.com/@aakashpydi/understanding-c-store-columnar-databases-and-big-data-analytics-aa669bb60f0

![1*xNYKI1azVyfzhXB-cIvKUw.png](Understanding%20C-Store%20Columnar%20Databases%20and%20Data%20%206ec9d29f6a4d493f941504b7069b76f7/1xNYKI1azVyfzhXB-cIvKUw.png)

From what I understand, the first prototype for a columnar database was introduced in a 2005 paper from MIT’s school of computer science and artificial intelligence, called [C-Store: A Column Oriented Database. (Stonebraker et al). MIT CSAIL.](http://db.csail.mit.edu/projects/cstore/vldb.pdf)

The key idea from this paper seems to be that, in columnar databases we store each column’s values sequentially in a database, as opposed to storing each row’s values sequentially. Let’s try to visualize this idea.

Some points to note regarding the example above:

- Notice that each block has values of different types (string, integer, etc).
- What happens if the row size is greater than a [block](https://docs.oracle.com/cd/B19306_01/server.102/b14220/logical.htm)? We will need to read more than a block to read a single row.
- Similarly, what happens if the row size is smaller than a [block](https://docs.oracle.com/cd/B19306_01/server.102/b14220/logical.htm)? In this case we will have inefficient use of disk space.
- Note that a data block is the smallest unit of data used by a database. See this link for more information: [Introduction to Data Blocks. Oracle.](https://docs.oracle.com/cd/B19306_01/server.102/b14220/logical.htm)
- This is a ‘write-optimized’ database as it has a very low cost to write a new record to disk. The DB can easily add a new block with the record’s data.

Some points to note regarding the example above:

- Notice that each block has the same data type. This turns out to be a significant advantage as the DB can use [compression techniques](http://db.csail.mit.edu/projects/cstore/abadisigmod06.pdf) to significantly reduce the disk usage and I/O.
- This is a ‘read optimized’ database, particularly in a big data analytics context (which is what we use the large datasets in our columnar database for). Consider how most queries only require a few of the column values. So when we have a large dataset, with many rows and columns, only retrieving the columns that we need to execute our analytics query is substantially more efficient than retrieving all the records in the database.

The original CSAIL paper notes that write optimized database systems are naturally ideal write heavy applications (such as [Online Transaction Processing](https://docs.microsoft.com/en-us/azure/architecture/data-guide/relational-data/online-transaction-processing) applications) whereas read optimized database systems are naturally ideal for read heavy applications (such as [Data Warehouses](https://aws.amazon.com/data-warehouse/)).

It should be evident why columnar databases are well suited for big data analytics architectures. They offer (i) significant data compression, and (ii) highly optimized read operations that are typically used for analytics jobs. My Director, Dan Woicke wrote about the value of using a columnar database to our team’s work here: [Cerner Advances Big Data Analytic Capabilities. Dan Woicke. CIO Review](https://hp.cioreview.com/cxoinsight/cerner-advances-big-data-analytic-capabilities-nid-11200-cid-59.html). There are more features that columnar databases offer which you can explore in the additional reading section below.