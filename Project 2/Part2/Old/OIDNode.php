<?php 
	/**
	* OIDNode
	*/
	class OIDNode
	{
		private $name;
		private $id; // Last number of OID
		private $oid;
		private $parent;
		private $children;
		
		function __construct($_id, $_name, $_oid)
		{
			$this->id = $_id;
			$this->name = $_name;
			$this->oid = $_oid;
			$this->children = array();
		}

		/* ================== Setters ================== */

		protected function set_name($_name){ $this->name = $_name; }

		protected function set_oid($_oid){ $this->oid = $_oid; }

		protected function set_parent($_parent){ $this->parent = $_parent; }


		protected function add_child($_id, $_child)
		{
			$children[$_id] = $_child;
		}

		protected function remove_child($_id)
		{
			unset($children[$_id]);
		}

		


		/* ================== Getters ================== */

		public function get_name(){ return $this->name; }

		public function get_oid(){ return $this->oid; }

		public function get_parent(){ return $this->parent; }

		public function get_children(){ return $this->children; }
	}
 ?>