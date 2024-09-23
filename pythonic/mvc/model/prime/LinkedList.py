class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


from threading import Lock


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0
        self.lock = Lock()

    def clear(self):
        self.head = None
        self.tail = None
        self.count = 0

    # effectively enqueing to tail
    def add(self, data):
        try:
            self.lock.acquire()
            new_node = Node(data)
            if not self.head:
                self.head = self.tail = new_node
            else:
                self.tail.next = new_node
                self.tail = new_node
            self.count += 1
        finally:
            self.lock.release()

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def enqueue(self, data):
        self.add(data)

    def dequeue(self):
        try:
            self.lock.acquire()
            if self.count == 0:
                return None
            elif self.count == 1:
                temp = self.head
                self.head = None
                self.tail = None
                self.count -= 1
                return temp.data
            else:
                temp = self.head
                self.head = self.head.next
                self.count -= 1
                return temp.data

        finally:
            self.lock.release()

    def remove(self, data):
        try:
            self.lock.acquire()
            current = self.head
            previous = None
            while current:
                # same as -> if id(current.data) == id(data):
                if current.data is data:
                    if previous:
                        previous.next = current.next
                        if current == self.tail:
                            self.tail = previous
                    else:
                        self.head = current.next
                        if current == self.tail:
                            self.tail = None
                    self.count -= 1
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
