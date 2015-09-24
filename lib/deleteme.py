#!/usr/bin/python

import sys
from PySide.QtGui import *


class TreeWidgetExample(QTreeWidget):
     """
     Tree widget to demostrate getting all parents of a clicked item and to
     demonstrate inserting new items around the clicked item.
     """

     def __init__(self, parent=None):
         super(TreeWidgetExample, self).__init__(parent)
         self.setColumnCount(2)
         self.setHeaderLabels(["Node", "Value"])
         self.build_tree()

     def build_tree(self):
         """Builds the tree according to your example on the Mailing 
list."""

         value = "example value"

         # root items
         nodeA = QTreeWidgetItem(self, ["A", value])
         nodeB = QTreeWidgetItem(self, ["B", value])

         # items on first child level
         node1 = QTreeWidgetItem(nodeA, ["1", value])
         node2 = QTreeWidgetItem(nodeA, ["2", value])
         node3 = QTreeWidgetItem(nodeB, ["3", value])
         node4 = QTreeWidgetItem(nodeB, ["4", value])

         # items on second child level
         QTreeWidgetItem(node1, ["a", value])
         QTreeWidgetItem(node1, ["b", value])
         QTreeWidgetItem(node2, ["c", value])
         QTreeWidgetItem(node2, ["d", value])
         QTreeWidgetItem(node3, ["e", value])
         QTreeWidgetItem(node3, ["f", value])
         QTreeWidgetItem(node4, ["g", value])
         QTreeWidgetItem(node4, ["h", value])

         self.itemClicked.connect(self.onItem)

     def onItem(self, item, column_nr):
         """
         Slot to be called if an item was clicked. Adds 2 new items to the
         tree and prints information about the item and it's parents.
         """

         # Comment this out, if you do not like having more and more 
			# items...
         self.addItems(item)

         print "Node %s clicked in column nr %d" % (item.text(0), column_nr)
         print "\tParents: " + str([str("Node %s" % node.text(0)) for 
node in self.getParents(item)])
         print

     def getParents(self, item):
         """
         Return a list containing all parent items of this item.
         The list is empty, if the item is a root item.
         """
         parents = []
         current_item = item
         current_parent = current_item.parent()

         # Walk up the tree and collect all parent items of this item
         while not current_parent is None:
             parents.append(current_parent)
             current_item = current_parent
             current_parent = current_item.parent()
         return parents

     def addItems(self, item):
         """
         Inserts 2 items for demonstration purpose:
             - 1 on the same level as the clicked item
             - 1 as a child of the clicked item
         """
         parents = self.getParents(item)
         direct_parent = parents[0] if parents else self
         QTreeWidgetItem(direct_parent, ["new1", "New node on same level"])
         QTreeWidgetItem(item, ["new2", "New node on child level"])


def main():

     app = QApplication(sys.argv)
     ex = TreeWidgetExample()
     ex.show()
     sys.exit(app.exec_())

if __name__ == '__main__':
     main()