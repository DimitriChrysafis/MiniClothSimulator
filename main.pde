ArrayList<Node> nodeArray = new ArrayList<>();
ArrayList<Link> linkArray = new ArrayList<>();
int gridCount = 60;
float friction = 0.99;
float forceMultiplier = 0.25;
float mouseRadius = 50;
float speedLimit;

void setup() {
  fullScreen(); 
  speedLimit = (width / gridCount) * 1.5;
  nodeArray = createNodes();
  linkArray = createLinks(nodeArray);
}

class Node {
  PVector pos, vel, force;
  boolean pinned;

  Node(float x, float y, boolean pinned) {
    pos = new PVector(x, y);
    vel = new PVector(0, 0);
    force = new PVector(0, 0);
    this.pinned = pinned;
  }

  void update() {
    if (pinned) return;
    PVector acc = PVector.mult(force, forceMultiplier);
    vel.add(acc);
    vel.limit(speedLimit);
    pos.add(vel);

    force.mult(0);
    vel.mult(friction);
  }
}

class Link {
  Node node1, node2;

  Link(Node node1, Node node2) {
    this.node1 = node1;
    this.node2 = node2;
  }

  void show() {
    line(node1.pos.x, node1.pos.y, node2.pos.x, node2.pos.y);
  }

  void update() {
    PVector difference = PVector.sub(node2.pos.copy(), node1.pos.copy());
    if (!node1.pinned) node1.force.add(difference);
    if (!node2.pinned) node2.force.sub(difference);
  }
}

ArrayList<Node> createNodes() {
  ArrayList<Node> nodes = new ArrayList<>();
  for (int j = 0; j < gridCount; j++) {
    for (int i = 0; i < gridCount; i++) {
      boolean pinned = (i == 0 || j == 0 || i == gridCount - 1 || j == gridCount - 1);
      float x = map(i, 0, gridCount - 1, 0, width - 1);
      float y = map(j, 0, gridCount - 1, 0, height - 1);
      nodes.add(new Node(x, y, pinned));
    }
  }
  return nodes;
}

ArrayList<Link> createLinks(ArrayList<Node> nodes) {
  ArrayList<Link> links = new ArrayList<>();
  for (int i = 0; i < nodes.size(); i++) {
    Node current = nodes.get(i);
    ArrayList<Node> rest = new ArrayList<>(nodes.subList(i + 1, nodes.size()));
    ArrayList<Node> neighbors = new ArrayList<>();
    
    for (Node target : rest) {
      if (current.pos.dist(target.pos) <= width / (gridCount - 1)) {
        neighbors.add(target);
      }
    }
    
    for (Node target : neighbors) {
      if (!current.pinned || !target.pinned) {
        links.add(new Link(current, target));
      }
    }
  }
  return links;
}

void draw() {
  background(255);
  stroke(0);

  if (mousePressed) grabNodesNearMouse();
  
  for (Link link : linkArray) {
    link.update();
  }
  
  for (Node node : nodeArray) {
    node.update();
  }
  
  for (Link link : linkArray) {
    link.show();
  }
}

void grabNodesNearMouse() {
  PVector mouse = new PVector(mouseX, mouseY);
  
  for (Node node : nodeArray) {
    if (!node.pinned && mouse.dist(node.pos) < mouseRadius) {
      node.pos.set(mouse.copy());
    }
  }
}
