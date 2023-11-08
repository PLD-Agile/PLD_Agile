from typing import List
from services.command.abstract_command import AbstractCommand
from src.services.singleton import Singleton
from reactivex import Observable
from reactivex.subject import BehaviorSubject, Subject


class CommandService(Singleton):
    __history: BehaviorSubject[List[AbstractCommand]] = BehaviorSubject([])
    __history_index: BehaviorSubject[int] = BehaviorSubject(-1)
    __on_execute: Subject[AbstractCommand] = Subject()
    __on_undo: Subject[AbstractCommand] = Subject()
    
    def __init__(self) -> None:
        self.__on_execute.subscribe(lambda command: print(f'Executed {command}'))
        self.__on_undo.subscribe(lambda command: print(f'Undone {command}'))
    
    def execute(self, command: AbstractCommand) -> None:
        self.__history.value = self.__history.value[:self.__history_index.value + 1] + [command]
        
        self.__history.on_next(self.__history.value)
        self.__history_index.on_next(len(self.__history.value) - 1)
        
        command.execute()
        self.__on_execute.on_next(command)
        
    def undo(self) -> None:
        if not self.__is_root():
            self.__history_index.on_next(self.__history_index.value - 1)
            self.__history.value[self.__history_index.value].undo()
            self.__on_undo.on_next(self.__history.value[self.__history_index.value])
            
    def redo(self) -> None:
        if self.__is_detached():
            self.__history_index.on_next(self.__history_index.value + 1)
            self.__history.value[self.__history_index.value].execute()
            self.__on_execute.on_next(self.__history.value[self.__history_index.value])
            
    def can_undo(self) -> Observable[bool]:
        return self.__history_index.map(lambda: not self.__is_root())
    
    def can_redo(self) -> Observable[bool]:
        return self.__history_index.map(lambda: self.__is_detached())
    
    def on_execute(self) -> Observable[AbstractCommand]:
        return self.__on_execute
    
    def on_undo(self) -> Observable[AbstractCommand]:
        return self.__on_undo
        
    def __is_root(self) -> bool:
        return self.__history_index.value == -1
    
    def __is_detached(self) -> bool:
        return self.__history_index.value != len(self.__history.value) - 1
