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
	// Match or keep below MySQL's wait_timeout (e.g., set lifetime to 3 minutes)
	db.SetConnMaxLifetime(3 * time.Minute)
	db.SetConnMaxIdleTime(1 * time.Minute)
	db.SetMaxOpenConns(25)
	db.SetMaxIdleConns(5)
	log.Println("Connected to MariaDB")
	return db
}
