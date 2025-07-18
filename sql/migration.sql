CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 3a6d19a95c40

CREATE TABLE tag (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    name VARCHAR(20) NOT NULL, 
    PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_tag_name ON tag (name);

CREATE TABLE uploaded_files (
    filename VARCHAR(255) NOT NULL, 
    filepath VARCHAR(255) NOT NULL, 
    file_size INTEGER NOT NULL, 
    content_type VARCHAR(100) NOT NULL, 
    id CHAR(32) NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE user (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    full_name VARCHAR(255), 
    email VARCHAR(255) NOT NULL, 
    hashed_password VARCHAR(255) NOT NULL, 
    is_active BOOL NOT NULL, 
    is_superuser BOOL NOT NULL, 
    PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_user_email ON user (email);

CREATE TABLE item (
    title VARCHAR(255) NOT NULL, 
    status INTEGER, 
    id INTEGER NOT NULL AUTO_INCREMENT, 
    owner_id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(owner_id) REFERENCES user (id) ON DELETE CASCADE
);

CREATE TABLE itemtaglink (
    item_id INTEGER NOT NULL, 
    tag_id INTEGER NOT NULL, 
    PRIMARY KEY (item_id, tag_id), 
    FOREIGN KEY(item_id) REFERENCES item (id), 
    FOREIGN KEY(tag_id) REFERENCES tag (id)
);

INSERT INTO alembic_version (version_num) VALUES ('3a6d19a95c40');

