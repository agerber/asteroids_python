from threading import Lock
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    # this is effectively a stack... with an additional delete method.
    def __init__(self):
        self.head = None
        self.count = 0
        self.lock = Lock()

    # has O(1): push at head
    def pushLeft(self, new_data):

        try:
            self.lock.acquire()
            new_node = Node(new_data)
            if self.count == 0:
                self.head = new_node
            else:
                temp = self.head
                self.head= new_node
                self.head.next = temp

            self.count += 1
        finally:
            self.lock.release()

    # has O(1): pop at head
    def popLeft(self):
        try:
            self.lock.acquire()
            if self.count == 0:
                return None
            elif self.count == 1:
                temp = self.head
                self.head = None
                self.count -= 1
                return temp.data
            else:
                temp = self.head
                self.head = self.head.next
                self.count -= 1
                return temp.data

        finally:
            self.lock.release()


    def delete(self, key):
        try:
            self.lock.acquire()

            if self.head is None:
                return

            # If the key is in head
            if self.head.data == key:
                self.head = self.head.next
                return

            # Find position of first occurrence of the key
            previous = None
            current = self.head
            while current:
                if current.data == key:
                    break
                previous = current
                current = current.next

            # If the key was found
            if current is not None:
                #skip over the current node in the chain, effectively orphaning the node
                previous.next = current.next
        finally:
            self.lock.release()


    # we need the __iter__ and __next__ methods to make this class iterable
    # def __iter__(self):
    #     #returning __iter__ object
    #     return self

    def __next__(self):
        if self.count == 0:
            raise StopIteration
        else:
            return self.head.next


    def printList(self):
        temp = self.head
        cnt = 0
        while (temp):
            print(str(cnt) + str(':') + str(temp.data))
            temp = temp.next
            cnt += 1

    def clear(self):
        self.head = None
        self.count = 0

# Code execution starts here
if __name__ == '__main__':

    list = Stack()
    print("50 deleted with no elements: " + str(list.delete(50)))
    #testing one element
    list.pushLeft(50)
    list.printList()
    print("50 deleted with one element: " + str(list.delete(50)))
    list.pushLeft(50)
    list.pushLeft(40)
    list.pushLeft(30)
    list.pushLeft(20)
    list.pushLeft(10)
    list.printList()
    print("30 deleted with many element: " + str(list.delete(30)))
    list.printList()
    print("50 last deleted with many element: " + str(list.delete(50)))
    list.printList()