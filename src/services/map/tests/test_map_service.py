from pytest import fixture
from src.services.map.map_service import MapService


class TestMapService:
    map_service: MapService
    
    @fixture(autouse=True)
    def setup_method(self):
        self.map_service = MapService.instance()
        
        yield
        
        MapService.reset()
    
    def test_should_create(self):
        assert self.map_service is not None
        
    def test_should_set_map(self):
        self.map_service.set_map("MAP")
        
        def on_next(map):
            assert map is not None
        
        self.map_service.map.subscribe(on_next)
        
    def test_should_clear_map(self):
        self.map_service.set_map("MAP")
        self.map_service.clear_map()
        
        def on_next(map):
            assert map is None
        
        self.map_service.map.subscribe(on_next)
        
    def test_should_add_marker(self):
        self.map_service.add_marker("MARKER")
        
        def on_next(markers):
            assert markers == ["MARKER"]
        
        self.map_service.markers().subscribe(on_next)
        
    def test_should_add_multiple_markers(self):
        self.map_service.add_marker("MARKER")
        self.map_service.add_marker("MARKER2")
        
        def on_next(markers):
            assert markers == ["MARKER", "MARKER2"]
        
        self.map_service.markers().subscribe(on_next)
        
    def test_should_clear_markers(self):
        self.map_service.add_marker("MARKER")
        self.map_service.clear_map()
        
        def on_next(markers):
            assert markers == []
        
        self.map_service.markers().subscribe(on_next)