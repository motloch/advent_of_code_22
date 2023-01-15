dat = list(map(int, open('20.txt', 'r').read().splitlines()))
n = len(dat)

# linked list class - also keep track of the order in which they should move
class Node:
    """
    Class for a node in a linked list
    """
    def __init__(self, value, move_order):
        self.value = value
        self.move_order = move_order
        self.next = None

def build_list(dat):
    """
    Build the linked list and return head
    """
    head = Node(dat[0], 0)
    last = head

    for i in range(1, n):
        newnode = Node(dat[i], i)
        last.next = newnode
        last = newnode

    foo = head
    res = [head.value]
    while foo.next:
        foo = foo.next
        res.append(foo.value)
    return head

def mix_list(head):
    """
    Performs the mixing and returns head of the resulting list
    """
    for i in range(n):
        
        # ABCDEFGH -> ABDEFGCH (move C) means:
        #   we need to find the previous element (B) - may be none, if we move head
        #   we need to find the element to move (C)
        #   we need to find the element before the new position (G) - can be wrapped around
        #   B.next = C.next
        #   C.next = G.next
        #   G.next = C

        # find B (or none) and C
        if head.move_order == i:
            B = None
            C = head
        else:
            B = head
            while B.next.move_order != i:
                B = B.next
            C = B.next

        # find G
        #    - we need to make n-1 hops to come back to the original position
        G = C
        moves_left = (C.value) % (n - 1)

        if moves_left > 0:

            while moves_left > 0:
                if not G.next:
                    G = head
                else:
                    G = G.next
                moves_left -= 1

            # perform the move
            if not B:
                head = C.next
            else:
                B.next = C.next

            C.next = G.next
            G.next = C

    return head

def evaluate(head):
    """
    Find the sum of 1000th, 2000th and 3000th number after zero
    """
    # find zero
    zero = head
    while zero.value != 0:
        zero = zero.next

    def value_x_nodes_after_node(node, x):
        temp = node
        while x > 0:
            if not temp.next:
                temp = head
            else:
                temp = temp.next
            x -= 1
        return temp.value

    v1 = value_x_nodes_after_node(zero, 1000)
    v2 = value_x_nodes_after_node(zero, 2000)
    v3 = value_x_nodes_after_node(zero, 3000)

    return v1 + v2 + v3

#####
# Problem 1
#####

head = build_list(dat)
head = mix_list(head)
print(evaluate(head))

#####
# Problem 2
#####

head = build_list(dat)
temp = head
while temp:
    temp.value *= 811589153
    temp = temp.next

for i in range(10):
    head = mix_list(head)
print(evaluate(head))
