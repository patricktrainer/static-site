# Duplicating a repository - GitHub Help

Created: Jan 30, 2020 8:55 PM
URL: https://help.github.com/en/github/creating-cloning-and-archiving-repositories/duplicating-a-repository

[GitHub.com](https://help.github.com/en/github) [Creating, cloning, and archiving repositories](https://help.github.com/en/github/creating-cloning-and-archiving-repositories) [Creating a repository on GitHub](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github) [Duplicating a repository](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/duplicating-a-repository) 

# Duplicating a repository

To duplicate a repository without forking it, you can run a special clone command, then mirror-push to the new repository.

[Mac](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/duplicating-a-repository) [Windows](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/duplicating-a-repository) [Linux](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/duplicating-a-repository) 

### [In this article](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/duplicating-a-repository)

- [Mirroring a repository](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/duplicating-a-repository)
- [Mirroring a repository that contains Git Large File Storage objects](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/duplicating-a-repository)
- [Mirroring a repository in another location](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/duplicating-a-repository)

Before you can duplicate a repository and push to your new copy, or *mirror*, of the repository, you must [create the new repository](https://help.github.com/en/articles/creating-a-new-repository) on GitHub. In these examples, `exampleuser/new-repository` or `exampleuser/mirrored` are the mirrors.

### [Mirroring a repository](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/duplicating-a-repository)

1.  

    Open Terminal.

2.   

    Create a bare clone of the repository.

    ```
    exampleuserold-repository
    ```

3.   

    Mirror-push to the new repository.

    ```
    old-repositoryexampleusernew-repository
    ```

4.   

    Remove the temporary local repository you created in step 1.

    ```
    old-repository
    ```

### [Mirroring a repository that contains Git Large File Storage objects](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/duplicating-a-repository)

1.  

    Open Terminal.

2.   

    Create a bare clone of the repository. Replace the example username with the name of the person or organization who owns the repository, and replace the example repository name with the name of the repository you'd like to duplicate.

    ```
    exampleuserold-repository
    ```

3.   

    Navigate to the repository you just cloned.

    ```
    old-repository
    ```

4.   

    Pull in the repository's Git Large File Storage objects.

    ```
    $ git lfs fetch --all
    ```

5.   

    Mirror-push to the new repository.

    ```
    exampleusernew-repository
    ```

6.   

    Push the repository's Git Large File Storage objects to your mirror.

    ```
    exampleuser/new-repository.git
    ```

7.   

    Remove the temporary local repository you created in step 1.

    ```
    old-repository
    ```

### [Mirroring a repository in another location](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/duplicating-a-repository)

If you want to mirror a repository in another location, including getting updates from the original, you can clone a mirror and periodically push the changes.

1.  

    Open Terminal.

2.   

    Create a bare mirrored clone of the repository.

    ```
    exampleuserrepository-to-mirror
    ```

3.   

    Set the push location to your mirror.

    ```
    repository-to-mirrorexampleusermirrored
    ```

As with a bare clone, a mirrored clone includes all remote branches and tags, but all local references will be overwritten each time you fetch, so it will always be the same as the original repository. Setting the URL for pushes simplifies pushing to your mirror. To update your mirror, fetch updates and push.

```
$ git fetch -p origin
$ git push --mirror
```