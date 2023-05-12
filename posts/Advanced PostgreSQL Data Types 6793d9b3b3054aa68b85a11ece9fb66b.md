# Advanced PostgreSQL Data Types

Created: May 27, 2020 4:07 PM
URL: https://info.crunchydata.com/blog/advanced-postgresql-data-types

![BlogImage-1.png](Advanced%20PostgreSQL%20Data%20Types%206793d9b3b3054aa68b85a11ece9fb66b/BlogImage-1.png)

This post is the second in a two-part series -- read the first here: [Going Back to Basics with PostgreSQL Data Types](https://info.crunchydata.com/blog/back-to-basics-with-postgresql-data-types).

In my last post, I shared some interesting (and at times surprising) things that I learned while digging into data types in PostgreSQL. Data types like numeric, integer, date, and char/varchar exist in every other relational database system since the need to work with such data is pretty much a given. The implementation may vary somewhat between systems, but generally there are standard ways you’ll want to process and analyze these types of data (e.g. perform mathematical calculations, find the length of a character string, cast from one type to another, etc).

In Postgres, we have a few more data types that may not be as well known even for experienced developers. Let’s take a quick look at arrays, enum, and range types.

### Array type

Arrays are likely something familiar, but in case you’re new to programming: it’s a data type meant to hold a collection of things. In some languages such as JavaScript, the array itself doesn’t have to hold values that are of the same data type. In Postgres, however, the array elements must all be of the same type - the table definition alludes to it:

```

CREATE TABLE countries_visited (
    person_name text,
    countries char(2)[]
);
```

As we can see above with the countries column, the array declaration must have the type name of the values that array will contain.

My internet searching seems to indicate that the array type is well suited for data that doesn’t have to strictly follow the rules of normalization. Take the example above (adapted from an example in the book [Troubleshooting PostgreSQL](https://g.co/kgs/Wr4dg3)): the countries_visited table stores a list of countries that each person has been to. If you wanted to normalize the data, you might go instead with a table that stores a combination of the person and each individual country visited, resulting in up to dozens of rows per person. You might also have a separate lookup table to link a two-letter country code to the full country name.

However, you may not have a need to maintain a lookup table (one could argue that a change in a country’s name doesn’t have to have a corresponding change in the list of visited countries). You may also find it more helpful to keep the list of countries visited in one record per person, instead of having to deal with potentially dozens of records per person. Using an array means you can do away with the extra table, and you don’t need to have multiple rows that pertain to the same person.

A few other examples I’ve come across where the array type could be used are: time series data (such as stock prices), tagging (for categories, or social media), readings or measurements taken from an instrument. Another good rule of thumb might be, if there are places in your application code where you’re using arrays and you often find yourself fetching entire data sets, storing the data as an array type could save you one more join against a lookup table.

### Enumerated (enum) type

I like to visualize enums this way: if I needed to populate a column with only values from a dropdown, what would be on that dropdown list? An enum type comes with its own set of acceptable values. (For the curious: enum types are registered in a system catalog called [pg_enum](https://www.postgresql.org/docs/current/catalog-pg-enum.html), where the enum values are represented internally as integers, and each enum “label” or name is stored as a character string.)

Some of you may be wondering: “But doesn’t that just sound like a CHECK constraint? Or perhaps foreign keys referencing a lookup table?” You’re not off track! These three are implemented differently, so one method might be a better fit for a particular use case than the others. For example, if my list of acceptable values is going to change constantly, I’d opt for a lookup table since it’s generally easier to modify a table than modify enums or constraints. So, it boils down to what your specific requirements are, although I do get the sense that it’s okay to view these three methods I tas multiple potential tools to solve a problem.

### Range type

You might say that a “range” can describe some set of values, i.e. when something is “within a range,” it is part of that set. So, it may not sound far off from enums on a surface level. I find it helpful to think of a range type's key characteristics as:

a) You can’t think of a range without thinking of its bounds (i.e. lower and upper limits).
b) The values within a range have an inherent sequence.

Technically, you could specify a range type where the limits do not exist (so the range is infinite), but even an unbounded range still has an order within it.

Range types work well for numeric data such as age, price, and weight; date/time data is also a typical candidate. I recommend checking out [Jonathan Katz’s blog](https://info.crunchydata.com/blog/author/jonathan-s-katz) post where he does a deep dive into [using the date range type](https://info.crunchydata.com/blog/range-types-recursion-how-to-search-availability-with-postgresql) for a scheduling application.

## These sound great! Now what?

These are just a few data types in PostgreSQL that you might not have worked with or been aware of. The cool thing about these more “advanced” data types is that they may help simplify your application code as well as let you write more concise database queries.

For example, there are some [built-in operators](https://www.postgresql.org/docs/current/functions-range.html) that you can use with range types that let you easily find the intersection of two ranges, or determine whether a value falls within the range. That’s not to say that you can’t arrive at the same answers if you had set up two individual columns that represent the range limits (a common one is start time and end time). But using the range operators combined with a specialized index such as [GiST](https://www.postgresql.org/docs/current/gist.html) may help get what you need in a quicker and more efficient way.

Our [second course on data types](https://learn.crunchydata.com/postgresql-devel/courses/basics/advdatatype) in the Crunchy Data interactive learning portal focuses on the above three types plus XML. It lets you play around with these data types with a little sample data, and it also introduces you to some helpful functions and operators that come with these data types.

Have you ever had to change your data structure and migrate from a common data type to a more advanced one like the above three? What was your decision-making process like, and how did the experience go for you? Comment below.

- [Tweet](https://twitter.com/share)
-