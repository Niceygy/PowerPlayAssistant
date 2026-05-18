package database

import "math"

// type StarSystem struct {
// 	System_name string
// 	Latitude    float64
// 	Longitude   float64
// 	Height      float64
// 	Is_anarchy  bool
// }

// type PowerData struct {
// 	System_name    string
// 	Shortcode      string
// 	State          string
// 	Control_points float64
// 	Points_change  float64
// }

type System struct {
	System_name    string
	Latitude       float64
	Longitude      float64
	Height         float64
	Is_anarchy     bool
	Shortcode      string
	State          string
	Control_points float64
	Points_change  float64
}

type Megaships struct {
	Name    string
	SYSTEM1 string
	SYSTEM2 string
	SYSTEM3 string
	SYSTEM4 string
	SYSTEM5 string
	SYSTEM6 string
}

func CreateDistanceStatement(user_system System) string {
	return `SQRT(
        POW(systems.latitude - ` + ftos(user_system.Latitude) + `, 2) +
        POW(systems.longitude  - ` + ftos(user_system.Longitude) + `, 2) +
        POW(systems.height    - ` + ftos(user_system.Height) + `, 2)
    ) AS distance`
}

func DistanceBetweenSystems(start string, end string) float64 {
	start_coords := GetSystemLocation(start)
	end_coords := GetSystemLocation(end)

	//x/y/z

	//diffrences
	xdist := end_coords.Latitude - start_coords.Latitude
	ydist := end_coords.Longitude - start_coords.Longitude
	zdist := end_coords.Height - start_coords.Height

	//square them
	xdistSqr := xdist * xdist
	ydistSqr := ydist * ydist
	zdistSqr := zdist * zdist

	//add them all
	sumOfSqares := xdistSqr + ydistSqr + zdistSqr

	distance := math.Sqrt(sumOfSqares)

	return math.Round(distance)
}
