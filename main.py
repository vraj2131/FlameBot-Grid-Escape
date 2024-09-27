from environment import ShipEnvironment

def main():
    # Create a ShipEnvironment instance with a 40x40 grid
    env = ShipEnvironment(grid_size=40)
    
    # Generate and visualize the environment
    env.create_environment()

if __name__ == "__main__":
    main()
