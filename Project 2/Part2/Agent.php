<?php 
	/**
	* Agent
	*/
	class Agent
	{
		protected $ip;
		protected $port;
		protected $version;
		protected $secname;

		protected $oidtree;

		
		function __construct($_ip, $_port, $_version, $_secname )
		{
			$this->set_ip($_ip);
			$this->set_port($_port);
			$this->set_version($_version);
			$this->set_secname($_secname);

			$this->oidtree = new OIDTree();
		}


		/* ================== Setters ================== */

		protected function set_ip($_ip){ $this->ip = $_ip; }

		protected function set_port($_port){ $this->port = $_port; }

		protected function set_version($_version){ $this->version = $_version; }

		protected function set_secname($_secname){ $this->secname = $_secname; }


		/* ================== Getters ================== */

		public function get_ip(){ return $this->ip; }

		public function get_port(){ return $this->port; }

		public function get_version(){ return $this->version; }

		public function get_secname(){ return $this->secname; }






	}
	

 ?>