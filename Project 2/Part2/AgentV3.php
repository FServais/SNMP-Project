<?php 
	/**
	* AgentV3
	*/
	class AgentV3 extends Agent
	{
		private $auth_proto;
		private $auth_pwd;
		private $priv_proto;
		private $priv_pwd;

		
		/* ================== Setters ================== */

		protected function set_auth_proto($_auth_proto){ $this->auth_proto = $_auth_proto; }

		protected function set_auth_pwd($_auth_pwd){ $this->auth_pwd = $_auth_pwd; }

		protected function set_priv_proto($_priv_proto){ $this->priv_proto = $_priv_proto; }

		protected function set_priv_pwd($_priv_pwd){ $this->priv_pwd = $_priv_pwd; }


		/* ================== Getters ================== */

		public function get_auth_proto(){ return $this->auth_proto; }

		public function get_auth_pwd(){ return $this->auth_pwd; }

		public function get_priv_proto(){ return $this->priv_proto; }

		public function get_priv_pwd(){ return $this->priv_pwd; }

	}
 ?>