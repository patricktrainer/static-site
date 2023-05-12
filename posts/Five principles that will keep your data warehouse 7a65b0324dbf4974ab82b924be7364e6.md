# Five principles that will keep your data warehouse organized

Created: Dec 4, 2019 11:53 AM
Tags: Data, Productivity
URL: https://blog.getdbt.com/five-principles-that-will-keep-your-data-warehouse-organized/

![Five%20principles%20that%20will%20keep%20your%20data%20warehouse%207a65b0324dbf4974ab82b924be7364e6/chuttersnap-kyCNGGKCvyw-unsplash.jpg](Five%20principles%20that%20will%20keep%20your%20data%20warehouse%207a65b0324dbf4974ab82b924be7364e6/chuttersnap-kyCNGGKCvyw-unsplash.jpg)

The natural state of the universe is chaos: entropy tends to increase in closed systems, and [there’s really nothing that we can do about that](https://www.multivax.com/last_question.html). So too is the nature of data warehouses: unless action is taken to maintain `order`in your data warehouse, it will inevitably spiral into a hard to navigate, hard to operate collection of objects that you’re too afraid to delete. While maintaining databases was once the job of dedicated Database Administrators, these days it’s common for no one (or rather, everyone) to be directly responsible for maintaining order in the database.

An actively maintained warehouse is a critical component of the highest functioning data teams. In a poorly maintained warehouse:

- Columns, tables, schemas and databases have inconsistent and possibly confusing names.
- Multiple users use the root user account to run simple select statements.
- The public schema and public role are heavily used.
- Objects within a schema have inconsistent ownership, privileges, and lineage.

And in such warehouses, it becomes difficult to answer seemingly simple questions, such as:

- How did this data get into the warehouse?
- Who has access to this data?
- What would happen if I were to drop this table? Is anyone using it? Do any downstream processes depend on it?
- Who ran that expensive query?
- What should I name this new user/schema/table/column?

A well maintained warehouse makes is easy for users to find relevant datasets and answers their own questions. While there’s no replacement for[really good data documentation](https://docs.getdbt.com/docs/documentation-website), the application of consistent conventions goes a long way towards empowering end-users.

This post reflects our best-practices for maintaining analytical data warehouses based on years of experience working with data across many organizations and data stacks. We’ve distilled our experiences into five principles that we feel to be true in any well maintained warehouse:

1. Use schemas to logically group together objects;
2. Use consistent and meaningful names for objects in a warehouse;
3. Use a separate user for each human being and application connecting to your data warehouse;
4. Grant privileges systematically; and
5. Limit access to superuser privileges.

For each principle, we’ve also shared our practices that help us implement these principles. Like much of what we write, these practices are opinionated, and won’t be right for every organization! We think they’re a great starting point for anyone who has suddenly found themselves in charge of administering a warehouse without having solved these problems before.

# Use schemas to logically group together objects

Schemas should be used to logically group together objects, similar to using directories when organizing files. Within a single schema:

- All relations (i.e. tables, views) should be created by the same process.
- All relations should have the same ownership.
- All relations should have the same privileges applied to them (see below).

We tend to:

- **Not** use the public schema.
- **For data sources:** Use one meaningfully-named schema per data source (for example `stripe` or `zendesk`). On Snowflake we often group these together in a raw database, while on Redshift, we might prefix all the data source schemas with “raw”, e.g. `raw_stripe`.
- **For production transformations** that should be queried by a BI tool: group models together by business area, for example, `core` (for shared data models), `marketing`, or `finance`.
- **For dev transformations**: Group models together based on their owner, for example in a schema named `dbt_claire`.

# **Use consistent and meaningful names for objects in a warehouse**

It’s been said many times over: *naming things is hard*.

In a data warehouse, you have a lot of objects to name — databases, schemas, relations, columns, users, and shared roles. On Snowflake you have even more things to name— warehouses (i.e. compute resources), stages, and pipes, for instance.

Using consistent naming patterns helps reduce the number of decisions to be made when creating objects, and can make it easier for a user to understand the structure of your warehouse. That being said, they can go too far! I’ve seen some warehouses that implement so many conventions that they become *harder* to navigate unless you know the rules (for example, `d_account_v.f_active` instead of `accounts.is_active`). As such, it’s also important to consider whether your names are meaningful!

Some of the patterns we use when naming objects in a warehouse include:

- Leveraging prefixes and suffixes to communicate patterns, for example, all timestamp columns end in `_at`, all dimension tables start with `dim_`, and metadata columns start with a leading underscore.
- Favoring readability over brevity, for example `customer_account_id` over `cust_acc_id`.
- Only using `snake_case` for names.

Once you’ve settled on your naming practices, we recommend codifying them into conventions, and sharing them with anyone using your warehouse. We’ve written down our specific naming conventions in our [dbt coding conventions](https://github.com/fishtown-analytics/corp/blob/master/dbt_coding_conventions.md#naming-and-field-conventions).

# Use a separate user for each human being and application connecting to your data warehouse

Before we dive into this, it’s worth noting that different data warehouses treat users, groups, and roles in very different ways (for anyone else that wants to fall down this rabbit hole, I wrote my findings up on [Discourse](https://discourse.getdbt.com/t/the-difference-between-users-groups-and-roles-on-each-data-warehouse/429)).

As such, it’s pretty hard to give advice here that isn’t tied to one specific data warehouse! For the remainder of this article, I’m going to abstract users, groups and roles into two entities:

- **User**: a single set of login credentials.
- **Shared role**: A group (on Redshift) or role (on Postgres or Snowflake) that a user can be a member of.

We always use a separate user for each human being and application connecting to a warehouse. We name these users in a way that makes sense, with names like `claire`, `drew`, `stitch`, `fivetran`, and `looker`. This makes it easier to manage access, debug when something goes wrong, and understand data lineage. Credentials should be securely stored, and only admins should have access to the passwords for application users.

With so many users, it can become difficult to manage privileges. Instead, we grant privileges to shared roles (more on this below), with users inheriting their privileges via their role membership. We tend to create a small number of shared roles, named `loader`, `transformer` and `reporter` — even if your data warehouse allows them, multi-level hierarchies for shared roles should be avoided, as they often become confusing to manage.

# Grant privileges systematically

Data warehouses provide fine-grained privileges —you can grant any combination of the following privileges to a user or a shared role (in fact, these are just a subset of your options!):

- On a database: usage, create
- On a schema: usage, create
- On a table: select, insert, update, delete, truncate, and references.

There’s a balance to be found between being too generous with privileges, where you grant `all` privileges to the `public` group, and being too restrictive with privileges, where a super user has to run a series of complex grant statements for every user that wants to run a select statement.

An overly permissive privilege scheme can lead to irreversible mistakes being made, while an overly restrictive privilege scheme can become a blocker for database users that just want to get their work done.

At the same time, you should consider the complexity of your privilege scheme — complex schemes can be difficult to maintain. With too much complexity, it becomes unclear who has access to what, and which grant statements should be run when a new user or schema is added.

We’ve found that a simplified privilege structure applied to shared roles provides a balanced level of control and is easy to maintain. In our data warehouses, we implement two privilege styles:

- `read-schema`: Ability to select from a schema and all relations within it.
- `create-schema`: Ability to create a schema in a database, and therefore create relations within it and have all privileges on those relations.

We then grant the following privileges to each of the shared roles in our warehouse:

- **loader**: `create-schema`
- **transformer:** `read-schema`, `create-schema`
- **reporter:** `read-schema` (limited to transformed schemas)

I’ve done a very implementation-focused writeup of the exact statements involved in setting up a warehouse in this way over on [Discourse](https://discourse.getdbt.com/t/the-exact-grant-statements-we-use-in-a-dbt-project/430).

Users should inherit their privileges via their memberships of these shared roles. This scheme is extremely easy to maintain — when a new user is added to our data warehouse, we only need to ensure they are members of the appropriate shared roles. Similarly, when a new schema is added to our data warehouse, we only need to grant privileges to the correct shared roles.

# Limit access to superuser privileges

Superuser privileges (for example, the ability to create users, or drop relations that do not belong to you), should be limited. Unless running a command that specifically requires these elevated privileges, users should use a user/role that does *not* have these privileges.

First, we limit access to the root user on Postgres and Redshift, or the AccountAdmin role on Snowflake. We only share this password on a need-to-know basis (but make sure it won’t be lost if someone leaves the organization!).

Further, we ensure users use a non-superuser as their default. The implementation of this varies across data warehouses based on how the warehouse handles inheritance:

- **Postgres**: Create a separate role with superuser privileges, and grant the role to individual users as required. Ensure this role does *not* have inheritance, so that users have to explicitly set their role to use their elevated privileges.
- **Redshift**: Create a separate user, `<user_name>_super` (e.g. `claire_super`) for each user that requires superuser privileges (superuser privileges can only be given to users, not groups). By default, users should connect to the warehouse with their non-super user credentials.
- **Snowflake**: Create a separate role with superuser privileges and grant it to the required users. Set each user’s default role to a role *other* than the superuser role.

# Additional configuration

- On most warehouses you can implement IP whitelisting. We recommend doing this when possible.
- If you happen to be setting up a Snowflake warehouse, my colleague [Jeremy Cohen](https://blog.fishtownanalytics.com/u/d1fca11d4b17?source=post_page---------------------------) has written a [fantastic guide](https://blog.fishtownanalytics.com/how-we-configure-snowflake-fc13f1eb36c4) on the topic.
- On Postgres and Redshift, there is much more that can be said about performance tuning — I’ll leave that for a separate article!

# Final thoughts

In short, good database administration can be summarized by two key themes:

1. **Keep it simple**
2. **Keep it consistent**

If you’re getting started with a data warehouse, spending some time upfront thinking about database administration will pay huge dividends for the future. If you’re trying to reverse the direction of entropy in an existing data warehouse, then there’s one last question: where are you going start? Let us hear it [on Slack](http://slack.getdbt.com/)!