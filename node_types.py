from node_type import NodeType


class NodeTypes:
    CHILDREN_WITH_CHILDREN = NodeType('Child with children', '>>')
    PARENT                 = NodeType('Parent',              '<<')
    PARENT_LIST_NODE       = NodeType('Parent list node',    '<>')
    LEAF                   = NodeType('Leaf',                '--')
    DUMMY                  = NodeType('Dummy',               '..')
