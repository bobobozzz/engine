#!/usr/bin/env python3

import pytest
from pin.kit.db.mysql import *
from pin.kit.db.redis import get_redis


def test_conn():
    db = get_db()
    ret = query(db, 'select 2 as num')
    assert not None is ret
    assert len(ret) == 1
    assert ret[0].get('num') == 2


def test_store_data():
    db = get_db()
    # Create test table
    create_test_table = """
        create table t_test_store(
            id int unsigned primary key auto_increment,
            field1 varchar(50) not null,
            created datetime default current_timestamp comment 'create record time',
            updated datetime on update current_timestamp comment 'update record time'
        )engine=InnoDB auto_increment=1000 default charset=utf8;
    """
    execute(db, create_test_table)

    # Insert one record
    insert(db, 'insert into t_test_store(field1) value("field1-value")')

    # Query one record
    r = query(db, 'select * from t_test_store where field1="field1-value"')
    assert len(r) == 1


def test_redis_access():
    redis = get_redis()
    redis().set("testkey-1", "test-data")
    assert "test-data" == redis().get("testkey-1")
    redis().delete("testkey-1")
    assert None == redis().get("testkey-1")
