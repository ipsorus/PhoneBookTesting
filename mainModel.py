# -*- coding: utf-8 -*-

from enum import Enum
import csv

class PhoneKind(Enum):
    unknown = 0
    mobile = 1
    private = 2
    home = 3
    office = 4
    work = 5
    
    def seralizeEnum(self):
        return self.name, self.value

    
class Phone:
    def __init__(self, number, kind):
        self.number = number
        self.kind = kind        
        
    def serializeCsv(self):
        return '{};{};'.format(self.number, PhoneKind(self.kind).name)
    
    def __repr__(self):
        return PhoneKind(self.kind).name + ': ' + self.number
    
class Person:
    def __init__(self, name = None, phones = None, email = None, idContact = None):
        self.name = name
        self.phones = phones
        self.email = email
        self.idContact = idContact
        
    def deserializeCsv(self, csvString):
        a = csvString.split(';')
        self.name = a[0]
        phonesCount = a[1]
        self.phones = []
        for i in range(int(phonesCount)):
            kind = PhoneKind.unknown.value
            kindStr = a[i*2 + 3]
            for kindName in PhoneKind:
                if kindStr in str(kindName):
                    kind = PhoneKind(kindName).value
                    break
            self.phones.append(Phone(a[i*2 + 2], kind))
        self.email = a[-2]
        self.idContact = a[-1]
        
    def addPhone(self, phone):
        self.phones.append(phone)

    def add_email(self, address):
        self.email = address
        
    def serializeCsv(self):
        s = '{};{};'.format(self.name, len(self.phones))
        for phone in self.phones:
            s += phone.serializeCsv()
        s += '{};{}'.format(self.email, self.idContact)
        #s += '{}'.format(self.idContact)
        return s
    
    def __repr__(self):
        s = ''
        if  self.name is not None:                        
            s += self.name + ', ' + str(self.phones) + ', ' + str(self.email) + ', ' + str(self.idContact)   
        return s
    
    
class PhoneBook():
    def __init__(self):
        self.items = []
        
    def addToBook(self, person):
        self.items.append(person)        
    
    def addToFile(self, filename):
        with open(filename,'w', encoding='utf-8') as book:
            for item in self.items:
                book.write(item.serializeCsv())
                book.write('\n')
        
    def readFile(self, file):
        with open(file,'r', encoding='utf-8') as book:
            self.items = []
            lines = book.readlines()
            for my_string in lines:
                p = Person()                
                p.deserializeCsv(my_string.strip())                
                self.items.append(p)
            return self.items
        
    def search(self, name):             
        result = []
        for item in self.items:            
            if name.lower() in item.name.lower(): 
                result.append(item)            
        return result
    
    def searchForEdit(self, name, idContact):             
        result = []
        for item in self.items:            
            if (name.lower() == item.name.lower()) and (idContact == item.idContact): 
                result.append(item)            
        return result
    
    def searchById(self, idContact):             
        result = []
        for item in self.items:            
            if idContact == item.idContact: 
                result.append(item)            
        return result

    def sortByName(self):
        a = self.items
        for i in range (len(a)):
            firstContact = i
            for j in range (i+1, len(a)):
                if str(a[j].name) < str(a[firstContact].name):
                    firstContact = j
            tmp = a[firstContact]
            a[firstContact] = a[i]
            a[i] = tmp
        return a
    
    def editName(self, name, newName):
        result = []
        self.name = name
        self.newName = newName
        
        for item in self.items:            
            if name == item.name: 
                item.name = newName
                result.append(item)
        return result
    
    def editContact(self, name, phones, email, idContact):
        result = []
        self.name = name
        self.phones = phones
        self.email = email
        
        for item in self.items:            
            if idContact == item.idContact: 
                item.name = name
                item.phones = phones
                item.email = email
                result.append(item)
        return result
    
    def deleteContact(self, name, idContact):
        self.name = name
        
        for item in self.items:            
            if (name == item.name) and (idContact == item.idContact): 
                self.items.remove(item)    

class Controller():  
    def __init__(self, phonesArray):        
        self.phonesArray = phonesArray
        self.items = self.phonesArray.items
        
    def addSimplePerson(self, name=None, phones=None, email=None, idContact = None):
        self.phonesArray.addToBook(Person(name, phones, email, idContact))  
    
    def sortByName(self):
        self.phonesArray.sortByName()
        #for a in self.phonesArray.items:
            #print(a)
    
    def search(self, name):        
        items = self.phonesArray.search(name)        
        if len(items) > 0:
            for a in items:
                return a
  
    def search_with_answ(self, name):        
        items = self.phonesArray.search(name)        
        if len(items) > 0:
            return items
        else:
            answ = False
            return answ
        
    def searchForEdit(self, name, idContact):        
        items = self.phonesArray.searchForEdit(name, idContact)        
        if len(items) > 0:
            for a in items:
                return a
    def searchById(self, idContact):        
        items = self.phonesArray.searchById(idContact)        
        if len(items) > 0:
            for a in items:
                return a    
    
    def editContact(self, name, phones, email, idContact):
        self.name = name
        self.phones = phones
        self.email = email
        items = self.phonesArray.searchById(idContact)
        if len(items) > 0:            
                editedItems = self.phonesArray.editContact(name, phones, email, idContact)
        for item in editedItems:
            return item   
        
    def deleteContact(self, name, idContact):
        self.name = name
        items = self.phonesArray.searchById(idContact)
        if len(items) > 0:            
            self.phonesArray.deleteContact(name, idContact)
            
    def addToFile(self, filename):
        self.phonesArray.addToFile(filename)
        
    def readFile(self, file):
        items = self.phonesArray.readFile(file)
        return items