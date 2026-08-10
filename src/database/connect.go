package database

import (
	"database/sql"
	"log"
	"os"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

var Db *sql.DB = OpenDatabase()

func OpenDatabase() *sql.DB {
	db, err := sql.Open("mysql", os.Getenv("DATABASE_CONNECTION_STRING"))
	if err != nil {
		log.Println("ERR" + err.Error())
		// panic(err)
	}
	err = db.Ping()
	if err != nil {
		log.Println("ERR" + err.Error())
	}
	// db.SetMaxOpenConns(10)
	db.SetConnMaxLifetime(1 * time.Minute)
	db.SetConnMaxIdleTime(1 * time.Minute)
	db.SetMaxOpenConns(10)
	db.SetMaxIdleConns(2)
	db.Stats()
	log.Println("Connected to MariaDB")
	return db
}
