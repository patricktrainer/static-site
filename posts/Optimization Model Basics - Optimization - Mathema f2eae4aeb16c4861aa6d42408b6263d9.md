# Optimization Model Basics - Optimization - Mathematics Library User's Guide - Documentation - Math, Statistics and Matrix Libraries for .NET in C#, VB and F#

Created: Mar 27, 2020 7:57 AM
URL: https://www.extremeoptimization.com/Documentation/Mathematics/Optimization/Optimization-Model-Basics.aspx

The optimization algorithms we have discussed so far are all unconstrained problems. The next three sections deal with constrained problems. Many of the constrained problems are derived from theoretical models where the solution is found by finding the configuration where a certain quantity reaches a maximum or a minimum.

In order to facilitate working with such models, the  **Extreme Optimization Numerical Libraries for .NET**  includes a framework for defining such models that allows for easier bookkeeping and managing the results.

All classes that implement optimization problems with constraints inherit from an abstract base class, [OptimizationModel](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.OptimizationModel.aspx).

An optimization model has three main components:

1. An objective function. This is the function that needs to be optimized.
2. A collection of decision variables. The solution to the optimization problem is the set of values of the decision variables for which the objective function reaches its optimal value.
3. A collection of constraints that restrict the values of the decision variables.

The [OptimizationModel](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.OptimizationModel.aspx) class provides a common API for defining and accessing variables and constraints, as well as other properties of each model.

We will now discuss each of these components in more detail.

Optimization problems can be classified in terms of the nature of the objective function and the nature of the constraints. Special forms of the objective function and the constraints give rise to specialized algorithms that are more efficient. From this point of view, there are four types of optimization problems, of increasing complexity.

An Unconstrained optimization problem is an optimization problem where the objective function can be of any kind (linear or nonlinear) and there are no constraints. These types of problems are handled by the classes discussed in the earlier sections.

A linear program is an optimization problem with an objective function that is linear in the variables, and all constraints are also linear. Linear programs are implemented by the [LinearProgram](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.LinearProgram.aspx) class.

A quadratic program is an optimization problem with an objective function that is quadratic in the variables (i.e. it may contain squares and cross products of the decision variables), and all constraints are linear. A quadratic program with no squares or cross products in the objective function is a linear program. Quadratic programs are implemented by the [QuadraticProgram](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.QuadraticProgram.aspx) class.

A nonlinear program is an optimization problem with an objective function that is an arbitrary nonlinear function of the decision variables, and the constraints can be linear or nonlinear. Nonlinear programs are implemented by the [NonlinearProgram](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.NonlinearProgram.aspx) class.

Finding the optimal values of the decision variables is the goal of solving an optimization model. In the optimization framework, variables are implemented by the [DecisionVariable](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.DecisionVariable.aspx) class.

Each variable has a [Name](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.OptimizationModelEntity.Name.aspx), which may be generated automatically. The [LowerBound](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.OptimizationModelEntity.LowerBound.aspx) and [UpperBound](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.OptimizationModelEntity.UpperBound.aspx) properties specify lower and upper bounds for the values the variable can take. After the solution of the model has been computed, the [Value](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.DecisionVariable.Value.aspx) property returns the value of the variable in the optimal solution.

[DecisionVariable](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.DecisionVariable.aspx) objects are created by calling one of the overloads of the optimization model's [AddVariable](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.OptimizationModel.AddVariable-Overloads.aspx) method. In some cases, they may also be created automatically.

An optimization model's variables can be accessed through its [Variables](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.OptimizationModel.Variables.aspx) property. Individual variables can be accessed by name or by position. The variable's [Position](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.OptimizationModelEntity.Position.aspx) property returns the variable's index in the collection.

Specific models may have specialized versions of the decision variables. For example, both linear and quadratic programs use variables of type [LinearProgramVariable](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.LinearProgramVariable.aspx), which inherits from [DecisionVariable](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.DecisionVariable.aspx) and has an extra [Cost](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.LinearProgramVariable.Cost.aspx) property that represents the coefficient of the variable in the linear portion of the objective function.

Constraints limit the possible values for the decision variables in an optimization model. There are several types of constraints. The classes that implement them all inherit from the [Constraint](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.Constraint.aspx) class.

Each constraint also has a [Name](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.OptimizationModelEntity.Name.aspx), which may again be generated automatically. The [LowerBound](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.OptimizationModelEntity.LowerBound.aspx) and [UpperBound](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.OptimizationModelEntity.UpperBound.aspx) properties specify lower and upper bounds for the value of the constraint. After the solution of the model has been computed, the [Value](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.DecisionVariable.Value.aspx) property returns the value of the constraint in the optimal solution.

There are two types of constraints: linear and nonlinear.

Linear constraints express that a linear combination of the decision variables must lie within a certain range. They are implemented by the [LinearConstraint](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.LinearConstraint.aspx) class. The coefficients can be accessed through the [Gradient](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.Constraint.Gradient.aspx) property. [LinearConstraint](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.LinearConstraint.aspx) objects are created by calling one of the overloads of the optimization model's [AddLinearConstraint](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.OptimizationModel.AddLinearConstraint-Overloads.aspx) method. In some cases, they may also be created automatically.

Nonlinear constraints express that the value of some arbitrary function of the decision variables must lie within a certain range. They are implemented by the [NonlinearConstraint](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.NonlinearConstraint.aspx) class. The constraint function can be accessed through the [ConstraintFunction](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.NonlinearConstraint.ConstraintFunction.aspx). The gradient of this function, which is needed during the optimization process, is the [FastConstraintGradient](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.NonlinearConstraint.FastConstraintGradient.aspx) If it is not supplied, a numerical approximation is used. [NonlinearConstraint](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.NonlinearConstraint.aspx) objects are created by calling one of the overloads of the optimization model's [AddNonlinearConstraint](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.NonlinearProgram.AddNonlinearConstraint-Overloads.aspx) method.

An optimization model's constraints can be accessed through its [Constraints](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.OptimizationModel.Constraints.aspx) property. Individual constraints can be accessed by name or by position. The variable's [Position](https://www.extremeoptimization.com/Documentation/Reference/Extreme.Mathematics.Optimization.OptimizationModelEntity.Position.aspx) property returns the constraint's index in the collection.

### Reference