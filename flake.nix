{
  description = "Nix flake for Home Assistant Migraine Integrator";

  inputs = {
    # Nixpkgs provides all the software packages
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    # flake-utils provides helper functions for multi-platform flakes
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # Import nixpkgs for the specific system (e.g., x86_64-linux)
        pkgs = nixpkgs.legacyPackages.${system};

        # Define Python environment with requested packages
        pythonEnv = pkgs.python311.withPackages (p: [
          p.requests
          p.flask # For the optional mock API
          # Add any other Python packages your script might need here
        ]);

      in {
        devShells.default = pkgs.mkShell {
          name = "migraine-integrator-shell";

          # Specify the packages available in the development shell
          packages = [
            pythonEnv # Our Python environment with dependencies
            pkgs.curl # Useful for testing HTTP requests
            pkgs.git # Good to have for development
          ];

          # Optional: Define environment variables when entering the shell
          # You can set defaults here, but ideally, you'd export them
          # before running nix develop or in a .envrc file.
          # HA_URL = "http://YOUR_HOME_ASSISTANT_IP:8123";
          # HA_ACCESS_TOKEN = "YOUR_LONG_LIVED_ACCESS_TOKEN"; # Only for event-based API, not webhooks

          # Commands to run when the shell is loaded (e.g., to activate venv)
          # For flakes, the pythonEnv is directly available, no separate venv activation needed
          shellHook = ''
            echo "---------------------------------------------------------"
            echo "Welcome to the Home Assistant Migraine Integrator shell!"
            echo "Python environment activated with requests and flask."
            echo "Remember to set HA_URL (and HA_ACCESS_TOKEN if using events) before running."
            echo "Example: export HA_URL="http://192.168.1.10:8123" "
            echo "---------------------------------------------------------"
          '';
        };
      });
}
