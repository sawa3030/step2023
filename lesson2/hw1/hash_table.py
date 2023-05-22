import random, sys, time, math

###########################################################################
#                                                                         #
# Implement a hash table from scratch! (⑅•ᴗ•⑅)                            #
#                                                                         #
# Please do not use Python's dictionary or Python's collections library.  #
# The goal is to implement the data structure yourself.                   #
#                                                                         #
###########################################################################

# Hash function.
#
# |key|: string
# Return value: a hash value
def calculate_hash(key):
    assert type(key) == str
    # Note: This is not a good hash function. Do you see why?
    # fixed calculate_hash. But this is working well just because most of the imput key is 0 to 100000000 number
    hash = 0
    for i in key:
        hash += ord('i')
        #char_num = ord(i)-ord('0')
        #hash += hash * 10 + char_num
    return hash


# An item object that represents one key - value pair in the hash table.
class Item:
    # |key|: The key of the item. The key must be a string.
    # |value|: The value of the item.
    # |next|: The next item in the linked list. If this is the last item in the
    #         linked list, |next| is None.
    def __init__(self, key, value, next):
        assert type(key) == str
        self.key = key
        self.value = value
        self.next = next


# The main data structure of the hash table that stores key - value pairs.
# The key must be a string. The value can be any type.
#
# |self.bucket_size|: The bucket size.
# |self.buckets|: An array of the buckets. self.buckets[hash % self.bucket_size]
#                 stores a linked list of items whose hash value is |hash|.
# |self.item_count|: The total number of items in the hash table.
class HashTable:

    # Initialize the hash table.
    def __init__(self, bucket_size):
        # Set the initial bucket size to 97. A prime number is chosen to reduce
        # hash conflicts.
        self.bucket_size = bucket_size
        self.buckets = [None] * self.bucket_size
        self.item_count = 0

    # Increase the table size
    def increase_table_size(self):
        new_hash_table = HashTable(self.bucket_size)
        new_hash_table = self

        new_size = self.item_count * 2 - 1
        self.bucket_size = new_size
        self.buckets = [None] * self.bucket_size

        for i in range (new_hash_table.bucket_size):
            item = new_hash_table.buckets[i]
            while item:
                new_item = item
                new_item.next = self.buckets[bucket_index]
                self.buckets[bucket_index] = new_item
                item = item.next
        print("increase", self.size(),self.item_count)

    # Put an item to the hash table. If the key already exists, the
    # corresponding value is updated to a new value.
    #
    # |key|: The key of the item.
    # |value|: The value of the item.
    # Return value: True if a new item is added. False if the key already exists
    #               and the value is updated.
    def put(self, key, value):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        # print(key, bucket_index)
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                item.value = value
                return False
            item = item.next
        new_item = Item(key, value, self.buckets[bucket_index])
        self.buckets[bucket_index] = new_item
        self.item_count += 1
        
        if self.item_count > 0.7 * self.bucket_size:
            self.increase_table_size()
        return True

    # Get an item from the hash table.
    #
    # |key|: The key.
    # Return value: If the item is found, (the value of the item, True) is
    #               returned. Otherwise, (None, False) is returned.
    def get(self, key):
        assert type(key) == str
        self.check_size() # Note: Don't remove this code.
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        while item:
            if item.key == key:
                print("get success", item.value)
                return (item.value, True)
            item = item.next
        return (None, False)

    # Decrease the table size
    def decrease_table_size(self):
        new_hash_table = HashTable(self.bucket_size)
        new_hash_table = self

        new_size = math.floor(self.item_count / 2)
        if new_size % 2 == 0:
            new_size -= 1
        self.bucket_size = new_size
        self.buckets = [None] * self.bucket_size

        for i in range (new_hash_table.bucket_size):
            item = new_hash_table.buckets[i]
            while item:
                new_item = item
                new_item.next = self.buckets[bucket_index]
                self.buckets[bucket_index] = new_item
                item = item.next

    # Delete an item from the hash table.
    #
    # |key|: The key.
    # Return value: True if the item is found and deleted successfully. False
    #               otherwise.
    def delete(self, key):
        assert type(key) == str
        #------------------------#
        # Write your code here!  #
        bucket_index = calculate_hash(key) % self.bucket_size
        item = self.buckets[bucket_index]
        item_before = None
        while item:
            if item.key == key:
                if item_before == None:
                    self.buckets[bucket_index] = item.next
                else:
                    item_before.next = item.next
                del item #これで消えているか不安、デストラクタ
                self.item_count -= 1
                # if self.item_count < 0.3 * self.bucket_size and self.item_count > 99:
                    # self.decrease_table_size()
                return True
            item_before = item
            item = item.next
        print(key, "not deleted")
        return False
        #------------------------#
        pass

    # Return the total number of items in the hash table.
    def size(self):
        return self.item_count

    # Check that the hash table has a "reasonable" bucket size.
    # The bucket size is judged "reasonable" if it is smaller than 100 or
    # the buckets are 30% or more used.
    #
    # Note: Don't change this function.
    def check_size(self):
        assert (self.bucket_size < 100 or
                self.item_count >= self.bucket_size * 0.3)


# Test the functional behavior of the hash table.
def functional_test():
    hash_table = HashTable(97)

    assert hash_table.put("aaa", 1) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.size() == 1

    assert hash_table.put("bbb", 2) == True
    assert hash_table.put("ccc", 3) == True
    assert hash_table.put("ddd", 4) == True
    assert hash_table.get("aaa") == (1, True)
    assert hash_table.get("bbb") == (2, True)
    assert hash_table.get("ccc") == (3, True)
    assert hash_table.get("ddd") == (4, True)
    assert hash_table.get("a") == (None, False)
    assert hash_table.get("aa") == (None, False)
    assert hash_table.get("aaaa") == (None, False)
    assert hash_table.size() == 4

    assert hash_table.put("aaa", 11) == False
    assert hash_table.get("aaa") == (11, True)
    assert hash_table.size() == 4

    assert hash_table.delete("aaa") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.size() == 3

    assert hash_table.delete("a") == False
    assert hash_table.delete("aa") == False
    assert hash_table.delete("aaa") == False
    assert hash_table.delete("aaaa") == False

    assert hash_table.delete("ddd") == True
    assert hash_table.delete("ccc") == True
    assert hash_table.delete("bbb") == True
    assert hash_table.get("aaa") == (None, False)
    assert hash_table.get("bbb") == (None, False)
    assert hash_table.get("ccc") == (None, False)
    assert hash_table.get("ddd") == (None, False)
    assert hash_table.size() == 0

    assert hash_table.put("abc", 1) == True
    assert hash_table.put("acb", 2) == True
    assert hash_table.put("bac", 3) == True
    assert hash_table.put("bca", 4) == True
    assert hash_table.put("cab", 5) == True
    assert hash_table.put("cba", 6) == True
    assert hash_table.get("abc") == (1, True)
    assert hash_table.get("acb") == (2, True)
    assert hash_table.get("bac") == (3, True)
    assert hash_table.get("bca") == (4, True)
    assert hash_table.get("cab") == (5, True)
    assert hash_table.get("cba") == (6, True)
    assert hash_table.size() == 6

    assert hash_table.delete("abc") == True
    assert hash_table.delete("cba") == True
    assert hash_table.delete("bac") == True
    assert hash_table.delete("bca") == True
    assert hash_table.delete("acb") == True
    assert hash_table.delete("cab") == True
    assert hash_table.size() == 0
    print("Functional tests passed!")


# Test the performance of the hash table.
#
# Your goal is to make the hash table work with mostly O(1).
# If the hash table works with mostly O(1), the execution time of each iteration
# should not depend on the number of items in the hash table. To achieve the
# goal, you will need to 1) implement rehashing (Hint: expand / shrink the hash
# table when the number of items in the hash table hits some threshold) and
# 2) tweak the hash function (Hint: think about ways to reduce hash conflicts).
def performance_test():
    hash_table = HashTable(97)

    for iteration in range(100):
        begin = time.time()
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.put(str(rand), str(rand))
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            assert hash_table.get(str(rand)) == (str(rand), True)
        end = time.time()
        print(hash_table.size(), hash_table.item_count)
        print("%d %.6f" % (iteration, end - begin))

    for iteration in range(100):
        random.seed(iteration)
        for i in range(10000):
            rand = random.randint(0, 100000000)
            hash_table.delete(str(rand))
        print(hash_table.size(), hash_table.item_count)

    print(hash_table.size(), hash_table.item_count)
    assert hash_table.size() == 0
    print("Performance tests passed!")


if __name__ == "__main__":
    functional_test()
    performance_test()
