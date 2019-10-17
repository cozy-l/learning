#encoding=utf-8

#单向链表
class Node():
    
    def __init__(self, value=None, node=None):
        self.next = node 
        self.value = value 

    def __str__(self):
        return str(self.value)

# 单向链表的反转 循环迭代法 主要是对三个变量的操作 pre head next
# 没操作一次都是 修改这三个指针变量
def reverse(head):
    if head == None or head.next==None:
        return head
    pre = None
    while head:
      next = head.next 
      head.next = pre
      pre = head
      head = next
    return pre

# 递归
# 翻转当前节点转换成先翻转下一个节点 直至最后，只剩下最后一个节点，可以很容易得到翻转结果
# 然后再层层上推
def reverse_1(head):
    if not head or not head.next:
        return head
    new_head = reverse_1(head.next)
    head.next.next = head
    head.next = None
    return new_head

def printlink(head):
    while head:
        print(head, end=' ') 
        head = head.next

if __name__ == '__main__':
    node_1 = Node(2)
    node_2 = Node(4, node_1)
    node_3 = Node(7, node_2)
    head = node_3
    printlink(head) 
   # head = reverse(head)
    head = reverse_1(node_3) 
    print()
    printlink(head)
    print()

    

          
