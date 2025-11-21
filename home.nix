{ config, pkgs, ... }:

{
  services.home-assistant = {
    enable = true;
    extraPackages =
      python3Packages: with python3Packages; [
        nextcord
      ];
    extraComponents = [
      "met"
      "esphome"
      "discord"
    ];
    config = {
      "automation ui" = "!include automations.yaml";
      default_config = { };
      http = {
        server_host = "0.0.0.0";
        server_port = 8123;
      };
    };
  };

  networking.firewall.allowedTCPPorts = [ 8123 ];
  systemd.tmpfiles.rules = [
    "f ${config.services.home-assistant.configDir}/automations.yaml 0755 hass hass"
  ];
}
