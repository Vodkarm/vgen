<!DOCTYPE html>
<html>
<head>
    <title>github.com/vodkarm/vgen</title>
    <style>
        body {
            color: white;
            font-family: Arial, sans-serif;
            background-color: #202324; /* Pretty background color */
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container {
            text-align: center;
            background-color: #181a1b;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        .rainbow-text {
            background: linear-gradient(
                to right,
                #7953cd 20%,
                #00affa 30%,
                #0190cd 70%,
                #764ada 80%
            );
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            text-fill-color: transparent;
            background-size: 500% auto;
            animation: textShine 3s ease-in-out infinite alternate;
        }
        
        @keyframes textShine {
            0% {
                background-position: 0% 50%;
            }
            100% {
                background-position: 100% 50%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <?php
        if (isset($_GET['data'])) {
            $data = $_GET['data'];
            $parts = explode("VGEN", $data);
            $service = $parts[1]; // After "VGEN"
            $actual_data = $parts[0]; // Before "VGEN"
            // Output the content of the "data" argument
            echo "<h1>Here is your <span class='rainbow-text'>". htmlspecialchars($service) . "</span> account !<br><h1>U/P: <span class='rainbow-text'>" . htmlspecialchars($actual_data) . "</span></h1>";
        } else {
            echo "<h1>No data could be parsed.</h1>";
        }
        ?>
    </div>
</body>
</html>
