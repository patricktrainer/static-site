# What is the front controller design pattern?

Created: Jun 17, 2020 4:45 PM
URL: https://www.educative.io/edpresso/what-is-the-front-controller-design-pattern

The **front controller [design pattern](https://www.educative.io/edpresso/design-patterns-in-java)** is used to refine the structure of an application which:

1.  

    Receives different types of requests from clients.

2.  

    Authenticates clients.

3.  

    Displays an output of the requests.

## Parts of the pattern

1.  

    The **front controller** receives a request from the client, authenticates it, and forwards the request to the *dispatcher*.

2.  

    The **dispatcher** determines the type of the request and allocates it to the relevant *handler*.

3.  

    The **handler** executes the business logic and updates the *view*.

4.  

    The **view** is the front-end container of the result produced from the request.

## UML diagram

[What%20is%20the%20front%20controller%20design%20pattern%200157185d2ea44ee7a102c83ec41269d6/6238711576526848](What%20is%20the%20front%20controller%20design%20pattern%200157185d2ea44ee7a102c83ec41269d6/6238711576526848)

```
#include <iostream>

using namespace std;

// Views:

class View1{
public:
    void update() {
        cout << "Bills payed." << endl;
    }
};

class View2{
public:
    void update() {
        cout << "Username updated." << endl;
    }
};

class View3{
public:
    void update() {
        cout << "Password changed." << endl;
    }
};

// Handlers:

class Handler1{
private:
    View1* view1;
    
public:
    Handler1() {
        view1 = new View1();
    }
    void updateView() {
        view1->update();
    }
};

class Handler2{
private:
    View2* view2;
    
public:
    Handler2() {
        view2 = new View2();
    }
    void updateView() {
        view2->update();
    }
};

class Handler3{
private:
    View3* view3;
    
public:
    Handler3() {
        view3 = new View3();
    }
    void updateView() {
        view3->update();
    }
};

// Dispatcher:
class Dispatcher{
private:
    Handler1* handler1;
    Handler2* handler2;
    Handler3* handler3;
    
public:
    Dispatcher(){
        handler1 = new Handler1();
        handler2 = new Handler2();
        handler3 = new Handler3();
    }
    void dispatch(string req) {
        if(req == "pay bills")
            handler1->updateView();
        else if(req == "update username")
            handler2->updateView();
        else if(req == "change password")
            handler3->updateView();
        else
            cout << "Invalid request!" << endl;
    }
};

// Controller:
class Controller{
private:
    Dispatcher* myDispatcher;
    bool authUser(string user) {
        if(user == "authentic")
            return true;
        else
            return false;
    }
public:
    Controller(){
        myDispatcher = new Dispatcher();
    }
    void forwardRequest(string u, string req) {
        if(authUser(u))
            myDispatcher->dispatch(req);
    }
};

int main(){
    Controller ctrl;
    ctrl.forwardRequest("authentic", "pay bills");
    
    return 0;
}

```