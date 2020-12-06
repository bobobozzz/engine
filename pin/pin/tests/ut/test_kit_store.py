#!/usr/bin/env python3

import pytest
import pin.kit.db.mysql as mysql
import pin.kit.db.redis as redis


def test_conn():
    ret = mysql.query('select 2 as num')
    assert not None is ret
    assert len(ret) == 1
    assert ret[0].get('num') == 2


def test_store_data():
    # Create test table
    create_test_table = """
        create table t_test_store(
            id int unsigned primary key auto_increment,
            field1 varchar(50) not null,
            created datetime default current_timestamp comment 'create record time',
            updated datetime on update current_timestamp comment 'update record time'
        )engine=InnoDB auto_increment=1000 default charset=utf8;
    """
    mysql.execute(create_test_table)

    # Insert one record
    mysql.insert('insert into t_test_store(field1) value("field1-value")')

    # Query one record
    r = mysql.query('select * from t_test_store where field1="field1-value"')
    assert len(r) == 1


def test_redis_access():
    redis.set("testkey-1", "test-data")
    assert "test-data" == redis.get("testkey-1")
    redis.delete("testkey-1")
    assert None == redis.get("testkey-1")
