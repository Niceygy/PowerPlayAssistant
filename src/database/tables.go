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

func CreateDistanceStatement(user_coords []float64) string {
	return `SQRT(
        POW(systems.longitude - ` + ftos(user_coords[0]) + `, 2) +
        POW(systems.latitude  - ` + ftos(user_coords[1]) + `, 2) +
        POW(systems.height    - ` + ftos(user_coords[2]) + `, 2)
    ) AS distance`
}

func DistanceBetweenSystems(start string, end string) float64 {
	start_coords := GetSystemLocation(start)
	end_coords := GetSystemLocation(end)

	//x/y/z

	//diffrences
	xdist := end_coords[0] - start_coords[0]
	ydist := end_coords[1] - start_coords[1]
	zdist := end_coords[2] - start_coords[2]

	//square them
	xdistSqr := xdist * xdist
	ydistSqr := ydist * ydist
	zdistSqr := zdist * zdist

	//add them all
	sumOfSqares := xdistSqr + ydistSqr + zdistSqr

	distance := math.Sqrt(sumOfSqares)

	return math.Round(distance)
}
