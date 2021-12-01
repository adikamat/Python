#pragma once
#include "States.h"
#include <vector>

/// Component class for composite design pattern used for transition, CG and condition
class IComponent
{
public:
  virtual bool evaluate() = 0;

};

/// Class to be derived by transition and condition group objects
class IComposite : public IComponent
{
public:
  bool evaluate() override
  {
    for (auto child : children)
    {
      child.evaluate();
    }
  }
private:
  std::vector<IComponent&> children;
};

class ITransition : public IComposite
{
public:
  virtual IStates& getNextState() = 0;
};

/// Condition objects are leaf objects and decorated by hypothesis evaluator and object class evaluators
class HypothesisDecorator : public IComponent
{
public:
  HypothesisDecorator(IComponent& cond/*, HypType hypType*/) : condition(cond)/*, hypType(hypType)*/
  {}

  bool evaluate() override
  {
    if (isHypothesisSatisfied())
    {
      condition.evaluate();
    }
  }

protected:
  virtual bool isHypothesisSatisfied() = 0;

private:
  IComponent& condition;
  // HypType hypType;
};

class ObjClassDecorator : public IComponent
{
public:
  ObjClassDecorator(IComponent& cond/*, ObjClass obj_class*/)
    : condition(cond)/*, hypType(hypType)*/
  {}

  bool evaluate() override
  {
    if (isObjClassSatisfied())
    {
      condition.evaluate();
    }
  }

protected:
  virtual bool isObjClassSatisfied() = 0;

private:
  IComponent& condition;
  // ObjClass obj_class;
};

class IStates
{
public:
  virtual void doTransition(IModule& module)
  {
    for (auto t : transList)
    {
      if(t.evaluate())
      {
        module.setState(t.getNextState());
        break;
      }
    }
  }

private:
  /// Hold list of transitions from current state
  std::vector<ITransition&> transList;
  /// Hold list of next states corresponding to transitions in "transList" member
  std::vector<IStates&> nextStates;
  // TODO : Add output handling
};

class IModule
{
public:
  IModule(IStates &initialState)
    : currState(initialState)
  {}

  virtual void run()
  {
    currState.doTransition(*this);

  }

  void setState(IStates& newState)
  {
    currState = newState;
  }

private:
  IStates& currState;
};

class StateMachineHandler
{
public:
  void addModule(IModule& module)
  {
    moduleList.push_back(module);
  }

  void run()
  {
    for (auto module : moduleList)
    {
      module.run();
    }
  }
private:
  std::vector<IModule&> moduleList;

};

