package database

import (
	"database/sql"
	"log"
	"os"

	_ "github.com/go-sql-driver/mysql"
)

var Db *sql.DB = OpenDatabase()

func OpenDatabase() *sql.DB {
	db, err := sql.Open("mysql", os.Getenv("DATABASE_CONNECTION_STRING"))
	if err != nil {
		log.Panic(err)
		// panic(err)
	}
	err = db.Ping()
	if err != nil {
		log.Panic(err.Error())
	}
	db.SetMaxOpenConns(10)
	log.Println("Connected to MariaDB")
	return db
}
