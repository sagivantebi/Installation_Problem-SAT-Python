Solving the Installation Problem using a script written in Python.

The solution derived from a reduction to a SAT problem.


Parsing Method:

* (Package1 -> (Depends1 And Not(Conflicts1)) And

* (Package2 -> (Depends2 And Not(Conflicts2)) And

 ...
 
* (PackageN -> (DependsN And Not(ConflictsN)) And

* Install



<img width="258" alt="installation-error" src="https://user-images.githubusercontent.com/84729141/233440783-8679faca-c852-4789-adc2-5b308963fc03.png">
