- 1 查看表创建了哪些索引:show index from table
- 2 mysql设计三范式 1）要求要有主键，并且每个字段原子性不可再分，2）要求所有非主键字段完全依赖主键，不能产生部分依赖
                  3）所有非主键字段和主键字段之间不能产生传递依赖

- 3 MySQL中delete,truncate与drop的区别:
    1) delete和truncate操作只删除表中数据，而不删除表结构；delete删除时对于auto_increment类型的字段，值不会从1开始，truncate可以实现删除数据后，auto_increment类型的字段值从1开始。但是drop语句将删 除表的结构被依赖的约束(constraint),触发器(trigger),索引(index); 依赖于该表的存储过程/函数将保留,但是变为invalid状态。
    2) 属于不同类型的操作，delete属于DML，这个操作会放到rollback segement中，事务提交之后才生效；如果有相应的trigger，执行的时候将被触发. 而truncate和drop属于DDL，操作立即生效，原数据不放到rollback segment中，不能回滚，操作不触发trigger。
    3) delete语句不影响表所占用的extent，高水线(high watermark)保持原位置不动。显然drop语句将表所占用的空间全部释放。truncate 语句缺省情况下见空间释放到 minextents个 extent,除非使用reuse storage; truncate会将高水线复位(回到最开始)。
    4) 执行速度，drop> truncate > delete
    5) 使用建议：
        完全删除表[drop]
        想保留表而将所有数据删除. 如果和事务无关[truncate]
        如果和事务有关,或者想触发trigger[delete]
