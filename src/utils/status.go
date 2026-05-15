package utils

const ED_SERVER_URL string = "https://ed-server-status.orerve.net/"

type ED_STATUS struct {
	status  string
	message string
	code    int
	product string
}

func getAppStatus() string {
	return ""
}

func getEDStatus() string {
	jsonData := HTTPGetJSON(ED_SERVER_URL)
	return "ED: " + jsonData["status"].(string)
}

func GetStatus() string {
	return getAppStatus() //+ ", " + getEDStatus()
}
