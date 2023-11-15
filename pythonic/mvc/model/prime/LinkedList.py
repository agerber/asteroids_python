class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


from threading import Lock
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.lock = Lock()

    def clear(self):
        self.head = None
        self.tail = None

    def add(self, data):
        try:
            self.lock.acquire()
            new_node = Node(data)
            if not self.head:
                self.head = self.tail = new_node
            else:
                self.tail.next = new_node
                self.tail = new_node
        finally:
            self.lock.release()

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def remove(self, data):
        try:
            self.lock.acquire()
            current = self.head
            previous = None
            while current:
                #same as -> if id(current.data) == id(data):
                if current.data is data:
                    if previous:
                        previous.next = current.next
                        if current == self.tail:
                            self.tail = previous
                    else:
                        self.head = current.next
                        if current == self.tail:
                            self.tail = None
                    return
                previous = current
                current = current.next
        finally:
            self.lock.release()

    def print_list(self):
        current = self.head
        while current:
            print(str(current.data), end=" -> ")
            current = current.next
        print("None")
