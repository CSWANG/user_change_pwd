Vagrant.require_version ">= 1.7.2"

# change default synced_folder for convenience
SYNCED_FOLDER = "/home/vagrant/mac"
ROOT_SYNCED_FOLDER = "/root/mac"

# expose ports from guest to host for convenience
#FORWARDED_PORT_RANGE = (10080..10300).to_a.push(10443).to_a.push(8080)

# external provision script files
#PROVISION_SCRIPTS = [ "pyLab.sh" ]

Vagrant.configure(2) do |config|

    config.vm.define "file01", primary: true do |node|

        node.vm.box = "ubuntu/trusty64"
        #node.vm.box_version = ">= 1.6.2"

        config.vbguest.auto_update = false
        config.ssh.insert_key = false
        node.vm.host_name = "file01"
        node.vm.network "private_network", ip: "10.0.0.10"

#        for i in FORWARDED_PORT_RANGE
#            node.vm.network "forwarded_port", guest: i, host: i
#        end

#        node.vm.network "forwarded_port", guest: 9200, host: 9200 
#        node.vm.network "forwarded_port", guest: 80, host: 20080

        node.vm.synced_folder ".", SYNCED_FOLDER
        node.vm.synced_folder ".", ROOT_SYNCED_FOLDER

        node.vm.provider "virtualbox" do |vb|
            vb.customize ["modifyvm", :id, "--cpus", "2"]
            vb.customize ["modifyvm", :id, "--memory", "4096"]
        end

        #node.vm.provision "shell", inline: <<-SHELL
        #    sudo apt-get update
        #    sudo apt-get install -y tree git wget lftp vim telnet
        #SHELL

        #for f in PROVISION_SCRIPTS
        #   node.vm.provision "shell", path: f
        #end
=begin
        config.vm.provision "shell" do |s|
            ssh_pub_key = File.readlines("/Users/csw/.ssh/id_rsa.pub").first.strip
            s.inline = <<-SHELL
            echo #{ssh_pub_key} >> /home/vagrant/.ssh/authorized_keys
            echo #{ssh_pub_key} >> /root/.ssh/authorized_keys
            SHELL
        end

=end
        config.vm.provision "ansible" do |ansible|
            ansible.playbook = "install-sw-base.yml"
            ansible.sudo = true
            #ansible.verbose          = "vvvvv"
            #ansible.inventory_path    = "vagrant_hosts_multi"
            #ansible.extra_vars        = "vars/extra_vars.yml"
            ansible.limit          = "all"
            ansible.host_key_checking = false
        end

    end

end
